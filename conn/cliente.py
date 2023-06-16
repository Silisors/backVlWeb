from motor.motor_asyncio import AsyncIOMotorClient

uri = "mongodb+srv://bmena100706:100706brandon@cluster0.uhngat9.mongodb.net/?retryWrites=true&w=majority"

# CONECCION AL SERVER
client = AsyncIOMotorClient(uri)

# ENVIA UN PING PARA CONFIRMAR LA CONEXION
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

db = client['data']
records = db['emails']
