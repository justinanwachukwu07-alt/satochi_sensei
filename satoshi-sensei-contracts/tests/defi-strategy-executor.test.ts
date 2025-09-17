import { Tx, Chain, Account, types } from "@hirosystems/clarinet-sdk";
import { assertEquals } from "vitest";

// @ts-ignore
Clarinet.test({
  name: "DeFi Strategy Executor - Initialize Protocols",
  async fn(chain: Chain, accounts: Map<string, Account>) {
    const deployer = accounts.get("deployer")!;

    // Initialize protocols
    const block = chain.mineBlock([
      Tx.contractCall(
        "defi-strategy-executor",
        "initialize-protocols",
        [],
        deployer.address
      )
    ]);

    assertEquals(block.receipts.length, 1);
    assertEquals(block.receipts[0].result, "(ok true)");
  }
});

Clarinet.test({
  name: "DeFi Strategy Executor - Execute Liquidity Provision",
  async fn(chain: Chain, accounts: Map<string, Account>) {
    const deployer = accounts.get("deployer")!;

    // Initialize protocols first
    chain.mineBlock([
      Tx.contractCall(
        "defi-strategy-executor",
        "initialize-protocols",
        [],
        deployer.address
      )
    ]);

    // Execute liquidity provision
    const block = chain.mineBlock([
      Tx.contractCall(
        "defi-strategy-executor",
        "execute-liquidity-provision",
        [
          types.utf8("alex"),
          types.utf8("STX"),
          types.utf8("USDA"),
          types.uint(1000000), // 1 STX
          types.uint(1000000)  // 1 USDA
        ],
        deployer.address
      )
    ]);

    assertEquals(block.receipts.length, 1);
    assertEquals(block.receipts[0].result, "u1"); // First execution ID
  }
});

Clarinet.test({
  name: "DeFi Strategy Executor - Execute Yield Farming",
  async fn(chain: Chain, accounts: Map<string, Account>) {
    const deployer = accounts.get("deployer")!;

    // Initialize protocols first
    chain.mineBlock([
      Tx.contractCall(
        "defi-strategy-executor",
        "initialize-protocols",
        [],
        deployer.address
      )
    ]);

    // Execute yield farming
    const block = chain.mineBlock([
      Tx.contractCall(
        "defi-strategy-executor",
        "execute-yield-farming",
        [
          types.utf8("arkadiko"),
          types.utf8("STX-USDA-POOL"),
          types.uint(5000000), // 5 STX
          types.uint(2592000)  // 30 days
        ],
        deployer.address
      )
    ]);

    assertEquals(block.receipts.length, 1);
    assertEquals(block.receipts[0].result, "u1");
  }
});

Clarinet.test({
  name: "DeFi Strategy Executor - Complete Execution",
  async fn(chain: Chain, accounts: Map<string, Account>) {
    const deployer = accounts.get("deployer")!;

    // Initialize protocols
    chain.mineBlock([
      Tx.contractCall(
        "defi-strategy-executor",
        "initialize-protocols",
        [],
        deployer.address
      )
    ]);

    // Execute a strategy
    chain.mineBlock([
      Tx.contractCall(
        "defi-strategy-executor",
        "execute-liquidity-provision",
        [
          types.utf8("velar"),
          types.utf8("STX"),
          types.utf8("USDA"),
          types.uint(2000000),
          types.uint(2000000)
        ],
        deployer.address
      )
    ]);

    // Complete the execution
    const block = chain.mineBlock([
      Tx.contractCall(
        "defi-strategy-executor",
        "complete-execution",
        [
          types.uint(1),
          types.uint(2100000) // 5% return
        ],
        deployer.address
      )
    ]);

    assertEquals(block.receipts.length, 1);
    assertEquals(block.receipts[0].result, "u1");
  }
});

Clarinet.test({
  name: "DeFi Strategy Executor - Get Execution",
  async fn(chain: Chain, accounts: Map<string, Account>) {
    const deployer = accounts.get("deployer")!;

    // Initialize protocols
    chain.mineBlock([
      Tx.contractCall(
        "defi-strategy-executor",
        "initialize-protocols",
        [],
        deployer.address
      )
    ]);

    // Execute a strategy
    chain.mineBlock([
      Tx.contractCall(
        "defi-strategy-executor",
        "execute-yield-farming",
        [
          types.utf8("alex"),
          types.utf8("STX-POOL"),
          types.uint(1000000),
          types.uint(86400)
        ],
        deployer.address
      )
    ]);

    // Get execution details
    const result = chain.callReadOnlyFn(
      "defi-strategy-executor",
      "get-execution",
      [types.uint(1)],
      deployer.address
    );

    assertEquals(result.result, `(some {
      id: u1,
      user: ${deployer.address},
      strategy-type: u2,
      amount: u1000000,
      protocol: "alex",
      status: "pending",
      created-at: u0,
      completed-at: none,
      fees-paid: u2500,
      returns: none
    })`);
  }
});

Clarinet.test({
  name: "DeFi Strategy Executor - Get Protocol Config",
  async fn(chain: Chain, accounts: Map<string, Account>) {
    const deployer = accounts.get("deployer")!;

    // Initialize protocols
    chain.mineBlock([
      Tx.contractCall(
        "defi-strategy-executor",
        "initialize-protocols",
        [],
        deployer.address
      )
    ]);

    // Get ALEX protocol config
    const result = chain.callReadOnlyFn(
      "defi-strategy-executor",
      "get-protocol-config",
      [types.utf8("alex")],
      deployer.address
    );

    assertEquals(result.result, `(some {
      enabled: true,
      min-amount: u1000000,
      max-amount: u1000000000,
      fee-rate: u25
    })`);
  }
});

Clarinet.test({
  name: "DeFi Strategy Executor - Update Protocol Config",
  async fn(chain: Chain, accounts: Map<string, Account>) {
    const deployer = accounts.get("deployer")!;

    // Initialize protocols
    chain.mineBlock([
      Tx.contractCall(
        "defi-strategy-executor",
        "initialize-protocols",
        [],
        deployer.address
      )
    ]);

    // Update protocol config
    const block = chain.mineBlock([
      Tx.contractCall(
        "defi-strategy-executor",
        "update-protocol-config",
        [
          types.utf8("alex"),
          types.bool(true),
          types.uint(2000000), // new min amount
          types.uint(2000000000), // new max amount
          types.uint(30) // new fee rate
        ],
        deployer.address
      )
    ]);

    assertEquals(block.receipts.length, 1);
    assertEquals(block.receipts[0].result, "(ok true)");
  }
});

Clarinet.test({
  name: "DeFi Strategy Executor - Invalid Protocol",
  async fn(chain: Chain, accounts: Map<string, Account>) {
    const deployer = accounts.get("deployer")!;

    // Initialize protocols
    chain.mineBlock([
      Tx.contractCall(
        "defi-strategy-executor",
        "initialize-protocols",
        [],
        deployer.address
      )
    ]);

    // Try to execute with invalid protocol
    const block = chain.mineBlock([
      Tx.contractCall(
        "defi-strategy-executor",
        "execute-liquidity-provision",
        [
          types.utf8("invalid-protocol"),
          types.utf8("STX"),
          types.utf8("USDA"),
          types.uint(1000000),
          types.uint(1000000)
        ],
        deployer.address
      )
    ]);

    assertEquals(block.receipts.length, 1);
    assertEquals(block.receipts[0].result, "(err u101)"); // ERR-INVALID-STRATEGY
  }
});
