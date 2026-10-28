#!/usr/bin/env python3
"""Kiểm logic nhận diện rollout xong/lỗi bằng dữ liệu Kubernetes mẫu, không gọi mạng.

  python scripts/test_rancher.py
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from rancher import (MASK, deployment_info, image_tag, mask_value, parse_since, pod_failure,  # noqa: E402
                     pod_info, rollout_done)


def pod(waiting=None, restarts=0, last_reason=None, phase="Running", ready=False):
    state = {"waiting": {"reason": waiting, "message": "back-off restarting failed container"}} if waiting else {"running": {}}
    last = {"terminated": {"reason": last_reason, "exitCode": 137}} if last_reason else {}
    return pod_info({
        "metadata": {"name": "svc-abc"},
        "spec": {"containers": [{"image": "reg/x/svc:20261028_1"}]},
        "status": {"phase": phase, "startTime": "2026-10-28T03:00:00Z",
                   "containerStatuses": [{"ready": ready, "restartCount": restarts, "image": "reg/x/svc:20261028_1",
                                          "state": state, "lastState": last}]},
    })


def deployment(replicas=1, updated=1, ready=1, available=1, unavailable=0, total=1, gen=2, observed=2, reason=None):
    cond = [{"type": "Progressing", "reason": reason or "NewReplicaSetAvailable", "message": "m"}]
    return deployment_info({
        "metadata": {"name": "svc", "generation": gen},
        "spec": {"replicas": replicas, "selector": {"matchLabels": {"app": "svc"}},
                 "template": {"spec": {"containers": [{"image": "reg:10187/x/svc:20261028_1"}]}}},
        "status": {"replicas": total, "updatedReplicas": updated, "readyReplicas": ready,
                   "availableReplicas": available, "unavailableReplicas": unavailable,
                   "observedGeneration": observed, "conditions": cond},
    })


class PodFailureTest(unittest.TestCase):
    def test_fatal_waiting_reasons_are_failures(self):
        for reason in ("CrashLoopBackOff", "ImagePullBackOff", "ErrImagePull", "CreateContainerConfigError"):
            self.assertIn(reason, pod_failure(pod(waiting=reason)))

    def test_starting_container_is_not_failure(self):
        self.assertIsNone(pod_failure(pod(waiting="ContainerCreating")))
        self.assertIsNone(pod_failure(pod()))

    def test_single_restart_is_tolerated_repeated_oom_is_failure(self):
        self.assertIsNone(pod_failure(pod(restarts=1, last_reason="OOMKilled")))
        self.assertIn("OOMKilled", pod_failure(pod(restarts=2, last_reason="OOMKilled")))

    def test_failed_phase(self):
        self.assertIsNotNone(pod_failure(pod(phase="Failed")))


class RolloutTest(unittest.TestCase):
    def test_complete(self):
        self.assertTrue(rollout_done(deployment()))

    def test_old_pod_still_present(self):
        self.assertFalse(rollout_done(deployment(total=2, unavailable=0)))

    def test_new_pod_not_ready(self):
        self.assertFalse(rollout_done(deployment(ready=0, available=0, unavailable=1)))

    def test_spec_not_observed_yet(self):
        self.assertFalse(rollout_done(deployment(gen=3, observed=2)))

    def test_deadline_exceeded_flag(self):
        self.assertTrue(deployment(reason="ProgressDeadlineExceeded")["deadline_exceeded"])

    def test_tag_parsing_ignores_registry_port(self):
        self.assertEqual(deployment()["tag"], "20261028_1")
        self.assertEqual(image_tag("reg:10187/x/svc"), "latest")


class MaskTest(unittest.TestCase):
    def test_sensitive_names_are_masked(self):
        for key in ("DB_PASSWORD", "OIDC_CLIENT_SECRET", "INTERNAL_SERVICE_TOKEN", "VNPT_CA_LICENSE_KEY",
                    "LIVEKIT_API_KEY", "JWT_PRIVATE_KEY", "TLS_CERT", "key"):
            self.assertEqual(mask_value(key, "abc"), MASK, key)

    def test_opaque_values_are_masked_even_with_innocent_names(self):
        self.assertEqual(mask_value("SOME_VALUE", "dGhpcyBpcyBhIGxvbmcgYmFzZTY0IHN0cmluZw0x"), MASK)
        self.assertEqual(mask_value("X", "-----BEGIN PRIVATE KEY-----\nabc"), MASK)

    def test_url_password_is_masked_but_url_kept(self):
        self.assertEqual(mask_value("DB_URL", "postgresql://app:s3cr3t@db:5432/x"), "postgresql://app:***@db:5432/x")

    def test_plain_config_stays_readable(self):
        for key, value in (("TZ", "Asia/Ho_Chi_Minh"), ("NOTARY_URI", "http://notary:8084"),
                           ("FEATURE_ENABLED", "true"), ("SMARTCA_SIGNING_PRICING_CODE", "1"),
                           ("KEYCLOAK_REALM", "congchung"), ("MONKEY_COUNT", "3")):
            self.assertEqual(mask_value(key, value), value, key)


class SinceTest(unittest.TestCase):
    def test_units(self):
        self.assertEqual(parse_since("90s"), 90)
        self.assertEqual(parse_since("30m"), 1800)
        self.assertEqual(parse_since("2h"), 7200)
        self.assertIsNone(parse_since(None))


if __name__ == "__main__":
    unittest.main(verbosity=1)
