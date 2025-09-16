;; Satoshi Sensei Core Contract Interface Trait

(define-trait ISatoshiSenseiCore
  ;; Strategy Management
  (create-strategy ((strategy-type (string-utf8 50)) (risk-score uint) (expected-apy uint) (amount uint)) (response uint uint))
  (execute-strategy ((strategy-id uint) (transaction-hash (string-utf8 100))) (response uint uint))
  (update-strategy-performance ((strategy-id uint) (actual-apy uint) (realized-pnl int) (fees-earned uint)) (response bool uint))
  
  ;; Configuration
  (set-protocol-fee-rate ((new-rate uint)) (response bool uint))
  (pause-contract () (response bool uint))
  
  ;; Read-only functions
  (get-strategy ((strategy-id uint)) (optional {
    id: uint,
    user: principal,
    strategy-type: (string-utf8 50),
    risk-score: uint,
    expected-apy: uint,
    amount: uint,
    status: (string-utf8 20),
    created-at: uint,
    executed-at: (optional uint),
    transaction-hash: (optional (string-utf8 100))
  }))
  
  (get-user-strategies ((user principal)) (optional (list 100 uint)))
  (get-strategy-performance ((strategy-id uint)) (optional {
    actual-apy: uint,
    realized-pnl: int,
    fees-earned: uint,
    last-updated: uint
  }))
  
  (get-contract-stats () {
    total-strategies: uint,
    total-volume: uint,
    protocol-fee-rate: uint
  })
)
