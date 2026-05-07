"""
Assignment 9: PKI-Based Identity Infrastructure (Toy Model)
------------------------------------------------------------
This is a simplified PKI simulation:
- CA creates a root secret (acts like CA private key)
- User identity has a public key
- CA signs user certificate using HMAC
- Certificate can be verified later

Important:
- This is educational and not production PKI.
"""

import hashlib
import hmac
import json
import secrets


class CertificateAuthority:
    def __init__(self, name):
        self.name = name
        self.ca_secret = secrets.token_bytes(32)  # toy CA signing key

    def sign_certificate(self, subject_name, subject_public_key):
        cert_data = {
            "issuer": self.name,
            "subject": subject_name,
            "public_key": subject_public_key,
        }
        cert_json = json.dumps(cert_data, sort_keys=True).encode()
        signature = hmac.new(self.ca_secret, cert_json, hashlib.sha256).hexdigest()

        return {
            "certificate": cert_data,
            "signature": signature,
        }

    def verify_certificate(self, cert_package):
        cert_json = json.dumps(cert_package["certificate"], sort_keys=True).encode()
        expected_sig = hmac.new(self.ca_secret, cert_json, hashlib.sha256).hexdigest()
        return hmac.compare_digest(expected_sig, cert_package["signature"])


def generate_identity(name):
    # Toy identity keys for learning.
    private_key = secrets.token_hex(32)
    public_key = hashlib.sha256(private_key.encode()).hexdigest()
    return {
        "name": name,
        "private_key": private_key,
        "public_key": public_key,
    }


if __name__ == "__main__":
    ca = CertificateAuthority("College-Root-CA")

    user = generate_identity("Student_A")
    cert_pkg = ca.sign_certificate(user["name"], user["public_key"])

    print("Generated Identity:")
    print(json.dumps({"name": user["name"], "public_key": user["public_key"]}, indent=2))

    print("\nIssued Certificate:")
    print(json.dumps(cert_pkg, indent=2))

    is_valid = ca.verify_certificate(cert_pkg)
    print("\nCertificate verification result:", is_valid)
