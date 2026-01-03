from beanie import Document
from pydantic import BaseModel

# Ici c'est le SCHÉMA (Ce que l'utilisateur envoie via l'API)
class CartRequest(BaseModel):
    productId: str 
    qty: int = 1

# Et là c'est le MODÈLE tel que stocké dans mongoDB
class Cart(Document):
    productId: str
    qty: int = 1

    class Settings:
        name = "cart" # Nom de la collection