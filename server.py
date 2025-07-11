# File: server.py

import flwr as fl
import os
from supabase import create_client, Client
from datetime import datetime

# Load Supabase credentials
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise Exception("SUPABASE_URL and SUPABASE_KEY must be set")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Log metrics to Supabase
def log_training_to_supabase(round_num, client_id, loss, val_loss, accuracy, kiosk_id):
    data = {
        "round": round_num,
        "client_id": client_id,
        "loss": loss,
        "val_loss": val_loss,
        "accuracy": accuracy,
        "kiosk_id": kiosk_id,
        "timestamp": datetime.utcnow().isoformat()
    }
    try:
        supabase.table("training_logs").insert(data).execute()
    except Exception as e:
        print("❌ Failed to log training data:", e)
class SaveMetricsStrategy(fl.server.strategy.FedAvg):
    def configure_fit(self, server_round, parameters, client_manager):
        client_instructions = super().configure_fit(server_round, parameters, client_manager)

        # Inject server_round into each client's config
        new_instructions = []
        for client, fit_ins in client_instructions:
            fit_ins.config["server_round"] = server_round
            new_instructions.append((client, fit_ins))

        return new_instructions

    def aggregate_fit(self, server_round, results, failures):
        aggregated_result = super().aggregate_fit(server_round, results, failures)
        for client_idx, (client, fit_res) in enumerate(results):
            metrics = fit_res.metrics
            if metrics:
                log_training_to_supabase(
                    round_num=server_round,
                    client_id=client_idx + 1,
                    loss=metrics.get("loss", 0),
                    val_loss=metrics.get("val_loss", 0),
                    accuracy=metrics.get("accuracy", 0),
                    kiosk_id=f"Kiosk_0{client_idx + 1}"
                )
        return aggregated_result

# Start Flower server
if __name__ == "__main__":
    strategy = SaveMetricsStrategy()
    fl.server.start_server(
        server_address="[::]:8080",
        config=fl.server.ServerConfig(num_rounds=3),
        strategy=strategy
    )
