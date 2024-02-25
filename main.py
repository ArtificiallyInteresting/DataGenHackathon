from dotenv import load_dotenv
import llm
import data
import time

load_dotenv()

def main():
    start = time.time()
    header, rows = data.input("commentsdata.csv")
    datagen = llm.llm()
    print("Starting data generation process.")
    new_data = datagen.generate_data(header, rows)

    # print(new_data)
    data.write("finaloutput.csv", header, new_data)
    print(f"Done in {time.time() - start:.2f} seconds")

if __name__ == "__main__":
    main()