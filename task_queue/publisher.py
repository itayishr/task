import json
import pika

def publish_scan_job(scan_id: int, repo_url: str, github_pat: str):
    connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq"))
    channel = connection.channel()

    channel.queue_declare(queue="scan_jobs", durable=True)

    message = {
        "scan_id": scan_id,
        "repo_url": repo_url,
        "github_pat": github_pat,
    }

    channel.basic_publish(
        exchange="",
        routing_key="scan_jobs",
        body=json.dumps(message),
        properties=pika.BasicProperties(
            delivery_mode=2,  # make message persistent
        ),
    )

    connection.close()