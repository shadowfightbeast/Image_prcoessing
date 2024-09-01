from app.celery_config import celery_app
from app.image_processor import fetch_image, process_image, save_image
import csv
import os
import uuid

UPLOAD_DIR = 'uploads/'

@celery_app.task
def process_images(request_id: str, file_path: str):
    from app.database import Session
    from app.models import ProcessingRequest
    from sqlmodel import select

    session = Session()

    processed_rows = []
    try:
        with open(file_path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                product_name = row['Product Name']
                input_urls = row['Input Image Urls'].split(',')
                output_urls = []
                
                for url in input_urls:
                    try:
                        image_bytes = fetch_image(url.strip())
                        processed_image = process_image(image_bytes)
                        output_path = os.path.join(UPLOAD_DIR, f"{uuid.uuid4()}.jpg")
                        save_image(output_path, processed_image)
                        output_urls.append(f"file://{output_path}")
                    except Exception as e:
                        print(f"Error processing image from {url}: {e}")
                        output_urls.append("Error")

                processed_rows.append({
                    "Serial Number": row['Serial Number'],
                    "Product Name": product_name,
                    "Input Image Urls": row['Input Image Urls'],
                    "Output Image Urls": ','.join(output_urls)
                })

        output_csv_path = os.path.join(UPLOAD_DIR, f"{request_id}_output.csv")
        with open(output_csv_path, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=["Serial Number", "Product Name", "Input Image Urls", "Output Image Urls"])
            writer.writeheader()
            writer.writerows(processed_rows)

        statement = select(ProcessingRequest).where(ProcessingRequest.request_id == request_id)
        processing_request = session.exec(statement).first()
        if not processing_request:
            raise Exception("Request ID not found")

        processing_request.status = "Completed"
        processing_request.output_csv_path = output_csv_path
        session.add(processing_request)
        session.commit()
    except Exception as e:
        print(f"Error processing images: {e}")
        processing_request.status = "Failed"
        session.add(processing_request)
        session.commit()
    finally:
        session.close()
