# Module M2 – Moteur de Scoring Multimodal

## Contexte
Ce module fait partie du projet **Application mobile de recherche basée sur l’Image et le Texte**.  
Le rôle du moteur multimodal est de comparer les requêtes utilisateur (texte ou image) avec les produits disponibles et de fournir un **score de pertinence** combinant les deux modalités.

---

## Objectifs
- Implémenter un moteur de scoring basé sur :
  - **Similarité textuelle** (embeddings NLP + cosine similarity).
  - **Similarité visuelle** (embeddings images + cosine/Euclidean distance).
- Fusionner les scores avec des pondérations ajustables (\(\alpha\) et \(\beta\)).
- Optimiser la recherche pour la rapidité et la précision (FAISS, PCA, threshold dynamique).
- Intégrer le moteur au backend via une API REST.

---

## Fonctionnement
1. **Similarité textuelle**  
   - Embeddings textuels (512 dimensions).  
   - Calcul de la similarité cosinus.  

2. **Similarité visuelle**  
   - Embeddings visuels (4096 dimensions).  
   - Distance cosinus ou euclidienne avec normalisation.  

3. **Fusion des scores**  
   - Formule :  
     

FinalScore = **α**TextScore +  **β**ImageScore

  
   - Avec **α** et **β** réglables selon les préférences utilisateur.  

4. **Optimisations**  
   - PCA pour réduire la dimensionnalité.  
   - Index FAISS (IVF, HNSW) pour accélérer les recherches.  
   - Threshold dynamique pour filtrer les résultats faibles.  

---

## Planification des tâches

| Phase | Tâches principales | Livrables |
|-------|-------------------|-----------|
| **Analyse & Design** | - Étudier les embeddings textuels et visuels<br>- Définir la formule de fusion et les paramètres | Spécification technique du moteur |
| **Implémentation Similarité Textuelle** | - Charger embeddings textuels<br>- Implémenter cosine similarity | Module de scoring texte |
| **Implémentation Similarité Visuelle** | - Charger embeddings visuels<br>- Implémenter cosine/Euclidean distance + normalisation | Module de scoring image |
| **Fusion Multimodale** | - Développer la fonction de fusion<br>- Paramétrer α et β | Fonction de scoring final |
| **Optimisations** | - Intégrer FAISS<br>- Tester PCA<br>- Implémenter threshold dynamique | Version optimisée du moteur |
| **Tests & Validation** | - Jeux de données tests<br>- Vérifier cohérence des scores<br>- Ajuster pondérations | Rapport de validation |
| **Intégration Backend (API)** | - Connecter moteur au backend (/search/multimodal)<br>- Vérifier compatibilité avec API | Endpoint fonctionnel |

---

## Prochaines étapes
- Assigner les tâches aux membres de l’équipe.  
- Démarrer l’implémentation en suivant la planification ci-dessus.  
