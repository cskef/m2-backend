# M2 – Moteur de scoring multimodal et Backend

## 1. Contexte
Le module M2 est chargé de comparer les requêtes utilisateur (texte et/ou image) avec les produits disponibles dans la base de données. Il calcule des scores de similarité textuelle et visuelle, puis les fusionne pour fournir un score final multimodal. Ce score permet de classer les produits par pertinence.  
Le backend est développé en **Python avec FastAPI** et utilise **MongoDB** comme base de données, avec l’ODM **Beanie** pour gérer les modèles.

---

## 2. Objectifs
- Implémenter un moteur de scoring multimodal basé sur :
  - Similarité textuelle (embeddings NLP).
  - Similarité visuelle (embeddings images).
- Fusionner les scores avec des pondérations ajustables (α et β).
- Exposer des endpoints REST pour la recherche et la gestion des produits/panier.
- Intégrer MongoDB pour stocker produits, paniers et embeddings.
- Préparer l’architecture pour des optimisations futures (FAISS, PCA, threshold dynamique).

---

## 3. Architecture Backend

### 3.1 Structure des dossiers
```
m2-backend/
├─ app/
│  ├─ main.py              # Point d’entrée FastAPI, init MongoDB/Beanie
│  ├─ api/                 # Routes HTTP
│  │  ├─ routes_text.py
│  │  ├─ routes_image.py
│  │  ├─ routes_multimodal.py
│  │  ├─ routes_product.py
│  │  └─ routes_cart.py
│  ├─ controllers/         # Logique métier intermédiaire
│  ├─ services/            # Services métier
│  │  ├─ text_service.py
│  │  ├─ image_service.py
│  │  ├─ fusion_service.py
│  │  ├─ product_service.py
│  │  └─ cart_service.py
│  ├─ core/                # Fonctions utilitaires (cosine, fusion, ranking)
│  ├─ models/              # Schémas MongoDB (Beanie)
│  ├─ dataset/             # Vectorisation pour le developement
│  └─ config.py            # Configuration globale
├─ requirements.txt        # Dépendances Python
└─ README.md               # Documentation projet
```

---

## 4. Endpoints REST

### Recherche
- **POST /search/text**  
  Entrée : `{ query: string, topK?: int }`  
  Sortie : liste de produits avec scores textuels.

- **POST /search/image**  
  Entrée : `multipart/form-data` avec `file: <image>` et `topK?: int`  
  Traitement : vectorisation de l’image côté backend.  
  Sortie : liste de produits avec scores visuels.

- **POST /search/multimodal**  
  Entrée : `multipart/form-data` avec `text: string`, `file: <image>`, `alpha: float`, `beta: float`, `topK?: int`  
  Traitement : vectorisation de l’image + embedding du texte → fusion des scores.  
  Sortie : liste de produits avec scores textuels, visuels et final.

### Produits
- **GET /product/{id}** : récupérer un produit par son ID.  
- **GET /product/all** : récupérer la liste complète des produits.

### Panier
- **POST /cart/add** : ajouter un produit au panier.  
- **POST /cart/remove** : retirer un produit du panier.  
- **GET /cart/list** : lister les produits du panier.

---

## 5. Modèles de données (MongoDB via Beanie)

### Product
- id, title, description, priceCFA, category, imageUrl.  
- Collection : `products`.

### Embedding
- productId, text (vecteur), image (vecteur).  
- Collection : `embeddings_text`, `embeddings_image`.

### Cart
- productId, qty.  
- Collection : `cart`.

---

## 6. Fonctionnement du moteur

### Similarité textuelle
- Embedding texte USE (512 dimensions).  
- Normalisation L2.
- Calcul : cosine similarity.  
- Score ∈ [0,1].

### Similarité visuelle
- Image uploadée → vectorisation Xception (4096 dimensions).  
- Normalisation L2.  
- Calcul : cosine similarity ou distance euclidienne.  
- Score ∈ [0,1].

### Fusion multimodale
\[
FinalScore = \alpha \cdot TextScore + \beta \cdot ImageScore
\]

### Optimisations futures
- PCA pour réduire la dimensionnalité.  
- FAISS pour accélérer la recherche vectorielle.  
- Threshold dynamique pour filtrer les résultats faibles.

---

## 7. Exemples de requêtes

### Recherche textuelle
```http
POST /search/text
Content-Type: application/json

{
  "query": "caméra IP 4MP",
  "topK": 5
}
```

### Recherche visuelle
```http
POST /search/image
Content-Type: multipart/form-data

file: <image.jpg>
topK: 5
```

### Fusion multimodale
```http
POST /search/multimodal
Content-Type: multipart/form-data

text: "point d'accès extérieur"
file: <image.jpg>
alpha: 0.6
beta: 0.4
topK: 5
```

### Produits
```http
GET /product/p2
GET /product/all
```

### Panier
```http
POST /cart/add
{ "productId": "p3", "qty": 1 }

POST /cart/remove
{ "productId": "p3" }

GET /cart/list
```

---

## 8. Ressources utiles
- Documentation Beanie ODM : [beanie-odm.dev](https://beanie-odm.dev/)  
- Documentation FastAPI : [fastapi.tiangolo.com/tutorial](https://fastapi.tiangolo.com/tutorial/)  
- Cosine similarity (explications) : [freeCodeCamp](https://www.freecodecamp.org/news/how-does-cosine-similarity-work/)  
- Cosine similarity (texte et images) : [NumberAnalytics](https://www.numberanalytics.com/blog/dive-into-cosine-similarity-text-images)  
- Télécharger MongoDB Community Server : [mongodb.com](https://www.mongodb.com/try/download/community?msockid=1a2b906218cf6652327784d71965679d)

---

## 9. Critères d’acceptation
- Les scores doivent être compris entre 0 et 1.  
- Les résultats doivent être triés par pertinence.  
- Les endpoints doivent respecter les contrats définis.  
- Les tests doivent valider la cohérence des scores et des réponses.  

## 10. Planification des taches et livrables
https://www.notion.so/2d98fe8a689a808f8ad5f6b7deeab9a6?v=2d98fe8a689a81edb186000c796fc1b7&source=copy_link