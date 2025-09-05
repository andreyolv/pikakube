import redis

HOST = '127.0.0.1'
PORT = 6379
PASSWORD = 'xxxxxxxxxxxxxx'

r = redis.Redis(
    host=HOST,
    port=PORT,
    password=PASSWORD,
    decode_responses=True
)

try:
    # Buscar valor
    valor = r.get("chave_exemplo")
    print("📦 Valor recuperado:", valor)

except redis.AuthenticationError:
    print("❌ Erro de autenticação: senha incorreta.")
except Exception as e:
    print("❌ Erro ao conectar ou operar no Redis:", str(e))
