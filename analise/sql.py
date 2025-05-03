import os
import re
import pandas as pd
import psycopg2 # type: ignore
from psycopg2 import sql # type: ignore
from dotenv import load_dotenv # type: ignore

# Load environment variables from the .env file
load_dotenv()

# === CONFIGURAÇÃO DO BANCO POSTGRES ===
db_config = {
    'dbname': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT')
}


def main():
    conn = psycopg2.connect(**db_config)
    cur = conn.cursor()

    # 1) Listar tabelas criadas
    print("Tabelas existentes no schema public:")
    cur.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public'
          AND table_type = 'BASE TABLE';
    """)
    for row in cur.fetchall():
        print(" -", row[0])

    # 2) Contar linhas em cada tabela
    for tbl in ('creation_metrics', 'search_metrics'):
        cur.execute(f"SELECT COUNT(*) FROM {tbl};")
        count = cur.fetchone()[0]
        print(f"\n {tbl} contém {count} registro(s).")

    # 3) Mostrar algumas linhas de exemplo
    for tbl in ('creation_metrics', 'search_metrics'):
        print(f"\nExemplos de dados em {tbl}:")
        df = pd.read_sql(f"SELECT * FROM {tbl} LIMIT 5;", con=conn)
        print(df.to_string(index=False))

    cur.close()
    conn.close()

if __name__ == '__main__':
    main()