import { Tx, Chain, Account, types } from "@hirosystems/clarinet-sdk";
import { assertEquals } from "vitest";

// @ts-ignore
Clarinet.test({
  name: "Satoshi Sensei Core - Create Strategy",
  async fn(chain: Chain, accounts: Map<string, Account>) {
    const deployer = accounts.get("deployer")!;
    const user = accounts.get("wallet_1")!;

    // Create a new strategy
    const block = chain.mineBlock([
      Tx.contractCall(
        "satoshi-sensei-core",
        "create-strategy",
        [
          types.utf8("liquidity_provision"),
          types.uint(75), // risk score
          types.uint(1200), // expected APY (12%)
          types.uint(1000000) // amount (1 STX)
        ],
        deployer.address
      )
    ]);

    assertEquals(block.receipts.length, 1);
    assertEquals(block.receipts[0].result, "u1"); // First strategy ID
  }
});

Clarinet.test({
  name: "Satoshi Sensei Core - Execute Strategy",
  async fn(chain: Chain, accounts: Map<string, Account>) {
    const deployer = accounts.get("deployer")!;

    // First create a strategy
    chain.mineBlock([
      Tx.contractCall(
        "satoshi-sensei-core",
        "create-strategy",
        [
          types.utf8("yield_farming"),
          types.uint(60),
          types.uint(1500),
          types.uint(2000000)
        ],
        deployer.address
      )
    ]);

    // Then execute it
    const block = chain.mineBlock([
      Tx.contractCall(
        "satoshi-sensei-core",
        "execute-strategy",
        [
          types.uint(1),
          types.utf8("0x1234567890abcdef")
        ],
        deployer.address
      )
    ]);

    assertEquals(block.receipts.length, 1);
    assertEquals(block.receipts[0].result, "u1");
  }
});

Clarinet.test({
  name: "Satoshi Sensei Core - Get Strategy",
  async fn(chain: Chain, accounts: Map<string, Account>) {
    const deployer = accounts.get("deployer")!;

    // Create a strategy
    chain.mineBlock([
      Tx.contractCall(
        "satoshi-sensei-core",
        "create-strategy",
        [
          types.utf8("staking"),
          types.uint(40),
          types.uint(800),
          types.uint(5000000)
        ],
        deployer.address
      )
    ]);

    // Get the strategy
    const result = chain.callReadOnlyFn(
      "satoshi-sensei-core",
      "get-strategy",
      [types.uint(1)],
      deployer.address
    );

    assertEquals(result.result, `(some {
      id: u1,
      user: ${deployer.address},
      strategy-type: "staking",
      risk-score: u40,
      expected-apy: u800,
      amount: u5000000,
      status: "pending",
      created-at: u0
    })`);
  }
});


Clarinet.test({
  name: "Satoshi Sensei Core - Get Contract Stats",
  async fn(chain: Chain, accounts: Map<string, Account>) {
    const deployer = accounts.get("deployer")!;

    // Create multiple strategies
    chain.mineBlock([
      Tx.contractCall(
        "satoshi-sensei-core",
        "create-strategy",
        [
          types.utf8("liquidity_provision"),
          types.uint(70),
          types.uint(1000),
          types.uint(1000000)
        ],
        deployer.address
      ),
      Tx.contractCall(
        "satoshi-sensei-core",
        "create-strategy",
        [
          types.utf8("yield_farming"),
          types.uint(80),
          types.uint(1500),
          types.uint(2000000)
        ],
        deployer.address
      )
    ]);

    // Get contract stats
    const result = chain.callReadOnlyFn(
      "satoshi-sensei-core",
      "get-contract-stats",
      [],
      deployer.address
    );

    assertEquals(result.result, `{
      total-strategies: u2,
      total-volume: u0,
      protocol-fee-rate: u25
    }`);
  }
});

Clarinet.test({
  name: "Satoshi Sensei Core - Unauthorized Access",
  async fn(chain: Chain, accounts: Map<string, Account>) {
    const user = accounts.get("wallet_1")!;

    // Try to create strategy as non-owner
    const block = chain.mineBlock([
      Tx.contractCall(
        "satoshi-sensei-core",
        "create-strategy",
        [
          types.utf8("liquidity_provision"),
          types.uint(75),
          types.uint(1200),
          types.uint(1000000)
        ],
        user.address
      )
    ]);

    assertEquals(block.receipts.length, 1);
    assertEquals(block.receipts[0].result, "(err u100)"); // ERR-UNAUTHORIZED
  }
});
