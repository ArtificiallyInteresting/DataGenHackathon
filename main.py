from dotenv import load_dotenv
import llm

load_dotenv()

def main():
    datagen = llm.llm()
    new_data = datagen.generate_data()
    print(new_data)
    out = open('data.json', 'w')
    out.write(new_data.content)
    out.close()

if __name__ == "__main__":
    main()