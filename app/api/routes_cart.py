from fastapi import APIRouter, HTTPException
from app.models.cart import Cart, CartRequest

router = APIRouter()

# 1. LISTER LE PANIER
@router.get("/list")
async def get_cart():
    cart_items = await Cart.find_all().to_list()
    return {"cart": cart_items}

# 2. AJOUTER AU PANIER
@router.post("/add")
async def add_to_cart(payload: CartRequest):

    existing_item = await Cart.find_one(Cart.productId == payload.productId)

    if existing_item:
        # Cas 1 : S'il existe, on augmente la quantité
        existing_item.qty += payload.qty
        await existing_item.save()
        return {"message": "Quantité mise à jour", "item": existing_item}
    else:
        # Cas 2 : S'il n'existe pas, on le crée
        new_item = Cart(productId=payload.productId, qty=payload.qty)
        await new_item.create()
        return {"message": "Produit ajouté", "item": new_item}

# 3. RETIRER DU PANIER
@router.post("/remove")
async def remove_from_cart(payload: CartRequest):

    existing_item = await Cart.find_one(Cart.productId == payload.productId)

    if not existing_item:
        raise HTTPException(status_code=404, detail="Produit non trouvé dans le panier")

    # On réduit la quantité si c'est supérieur à 1
    if existing_item.qty > 1:
        existing_item.qty -= 1
        await existing_item.save()
        return {"message": "Quantité décrémentée", "qty": existing_item.qty}
    else:#Sinon, on supprime
        await existing_item.delete()
        return {"message": "Produit retiré du panier"}