"""
Bitcoin Transaction Policy Analyzer
Author: Edwin Tanui

Analyzes Bitcoin transactions from a mempool *policy* perspective
(not consensus), focusing on standardness, fees, and dust outputs.
"""

DUST_LIMIT_SATS = 546
MIN_RELAY_FEE_RATE = 1  # sat/vB (simplified)
MAX_STANDARD_TX_WEIGHT = 400_000


def is_dust(value_sats: int) -> bool:
    return value_sats < DUST_LIMIT_SATS


def calculate_fee(input_sum: int, output_sum: int) -> int:
    return input_sum - output_sum


def fee_rate_sats_per_vb(fee: int, vbytes: int) -> float:
    if vbytes == 0:
        return 0.0
    return fee / vbytes


def analyze_outputs(outputs):
    issues = []
    for index, value in enumerate(outputs):
        if is_dust(value):
            issues.append(
                f"Output {index}: dust output ({value} sats < {DUST_LIMIT_SATS})"
            )
    return issues


def policy_checks(tx):
    """
    Policy checks affect relay and mining, not consensus validity.
    """
    issues = []

    if tx["weight"] > MAX_STANDARD_TX_WEIGHT:
        issues.append("Transaction exceeds standard weight limit")

    issues.extend(analyze_outputs(tx["outputs"]))

    fee = calculate_fee(tx["input_sum"], sum(tx["outputs"]))
    feerate = fee_rate_sats_per_vb(fee, tx["vbytes"])

    if feerate < MIN_RELAY_FEE_RATE:
        issues.append(
            f"Fee rate too low ({feerate:.2f} sat/vB < {MIN_RELAY_FEE_RATE})"
        )

    return issues, fee, feerate


def analyze_transaction(tx):
    print("=== Bitcoin Mempool Policy Analysis ===")
    print(f"Version: {tx['version']}")
    print(f"Inputs total: {tx['input_sum']} sats")
    print(f"Outputs total: {sum(tx['outputs'])} sats")
    print(f"Virtual size: {tx['vbytes']} vB")
    print(f"Weight: {tx['weight']}")

    issues, fee, feerate = policy_checks(tx)

    print(f"\nFee: {fee} sats")
    print(f"Fee rate: {feerate:.2f} sat/vB\n")

    if issues:
        print("Policy issues detected:")
        for issue in issues:
            print("-", issue)
    else:
        print("Transaction is policy-standard and relayable")


if __name__ == "__main__":
    # Example simulated transaction
    sample_tx = {
        "version": 2,
        "input_sum": 150_000,
        "outputs": [100_000, 300],  # includes dust
        "vbytes": 180,
        "weight": 720
    }

    analyze_transaction(sample_tx)
