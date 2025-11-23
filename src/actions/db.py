import psycopg2
import os
import uuid
from typing import Text

database_url = os.getenv('DATABASE_URL')

def conexion():
  if not database_url:
    raise ValueError("DATABASE_URL no está definida")
  
  return psycopg2.connect(database_url)

def get_user(idUser: Text):
  try:
    conn = conexion()
    cursor = conn.cursor()

    with conn:
      with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM users WHERE id = %s", (idUser,))
        result = cursor.fetchone()

    conn.close()
    if result:
      return {"success": True, "user": result}
    else:
      return {"success": False, "user": "no encontrado"}
  except Exception as e:
    print(f"Error al conectar con la base de datos: {str(e)}")
    return {"success": False, "error": str(e)}


def create_conversation(idUser: Text, received: Text, chatbot: Text):
  try:
    user_uuid = str(uuid.UUID(idUser))
    conn = conexion()
    cursor = conn.cursor()

    with conn:
      with conn.cursor() as cursor:
        cursor.execute("INSERT INTO messages (received, chatbot, id_user)  VALUES  (%s, %s, %s) RETURNING id", (received, chatbot, user_uuid))
        result = cursor.fetchone()[0]
        conn.commit()

    cursor.close()
    conn.close()
    if result:
      return {"success": True, "conversation": result}
    else:
      return {"success": False, "conversation": "no encontrado"}
  except Exception as e:
    print(f"Error al conectar con la base de datos: {str(e)}")
    return {"success": False, "error": str(e)}
  
