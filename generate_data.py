import pandas as pd
import random
from faker import Faker

fake = Faker()

def generate_kavach_data(n_samples=1000):
    data = []
    for _ in range(n_samples):
        # Normal behavior: Calls during day, shorter duration
        hour = random.randint(8, 22) 
        duration = random.randint(30, 300) # seconds
        is_spoofed = 0 # Normal
        data.append([hour, duration, is_spoofed])
    
    # Add 50 "Scam/Anomalous" samples
    for _ in range(50):
        hour = random.randint(0, 5) # Calls at midnight (Suspicious)
        duration = random.randint(600, 1800) # Very long (Suspicious)
        is_spoofed = 1 
        data.append([hour, duration, is_spoofed])
        
    df = pd.DataFrame(data, columns=['call_hour', 'duration_sec', 'label'])
    df.to_csv('call_logs.csv', index=False)
    print("✅ synthetic dataset 'call_logs.csv' created!")

generate_kavach_data()