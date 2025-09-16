;; Satoshi Sensei Core Contract Interface Trait

(define-trait ISatoshiSenseiCore
  (create-strategy ((strategy-type (string-utf8 50)) (risk-score uint) (expected-apy uint) (amount uint)) (response uint uint))
  (execute-strategy ((strategy-id uint) (transaction-hash (string-utf8 100))) (response uint uint))
  (get-strategy ((strategy-id uint)) (optional uint))
  (get-contract-stats () uint)
)