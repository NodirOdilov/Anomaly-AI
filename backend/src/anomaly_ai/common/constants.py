NETWORK_LABEL_BENIGN = "BENIGN"
NETWORK_SUSPICIOUS_LABELS = frozenset({"HTTP_ATTACK", "UDP_ATTACK", "SUSPICIOUS"})

WAF_ATTACK_TYPES = frozenset(
    {
        "benign",
        "sql_injection",
        "xss",
        "path_traversal",
        "command_injection",
        "generic_injection",
    }
)
