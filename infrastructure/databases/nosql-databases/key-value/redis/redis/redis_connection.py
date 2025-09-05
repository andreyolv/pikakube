import redis

HOST = '127.0.0.1'
PORT = 6379
PASSWORD = 'xxxxxxxxxxx'

r = redis.Redis(
    host=HOST,
    port=PORT,
    password=PASSWORD,
    decode_responses=True
)

try:
    r.ping()
    print("✅ Conectado ao Redis com sucesso!")

    # Salvar valor
    r.set("chave_exemplo", "valor123")
    print("🔐 Valor salvo!")

    # Buscar valor
    valor = r.get("chave_exemplo")
    print("📦 Valor recuperado:", valor)

except redis.AuthenticationError:
    print("❌ Erro de autenticação: senha incorreta.")
except Exception as e:
    print("❌ Erro ao conectar ou operar no Redis:", str(e))
