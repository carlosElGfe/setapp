

def my_scheduled_job():
    with open('data.txt', 'w', encoding='utf-8') as f:
        f.write("job done")
        f.close()