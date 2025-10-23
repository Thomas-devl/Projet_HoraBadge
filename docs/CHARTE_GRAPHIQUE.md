# Charte Graphique HoraBadge

## 🎨 Palette de Couleurs

### Couleurs Principales
- **Bleu Principal** : `#1E88E5` 
  - Usage : Boutons primaires, en-têtes, liens, éléments interactifs
  - RGB : rgb(30, 136, 229)
  
- **Bleu Foncé** : `#1565C0`
  - Usage : Hover sur les boutons primaires, titres importants
  - RGB : rgb(21, 101, 192)
  
- **Bleu Clair** : `#E3F2FD`
  - Usage : Arrière-plans subtils, hover sur éléments secondaires
  - RGB : rgb(227, 242, 253)

### Couleurs Secondaires
- **Blanc** : `#FFFFFF`
  - Usage : Texte sur fond bleu, cartes, conteneurs principaux
  
- **Gris Clair** : `#F5F5F5`
  - Usage : Arrière-plan général, zones secondaires
  - RGB : rgb(245, 245, 245)
  
- **Gris Moyen** : `#9E9E9E`
  - Usage : Bordures, séparateurs
  - RGB : rgb(158, 158, 158)
  
- **Gris Foncé** : `#424242`
  - Usage : Texte secondaire, icônes
  - RGB : rgb(66, 66, 66)
  
- **Noir** : `#212121`
  - Usage : Texte principal
  - RGB : rgb(33, 33, 33)

### Couleurs d'État
- **Succès (Vert)** : `#4CAF50`
  - Usage : Messages de succès, validations, états positifs
  - RGB : rgb(76, 175, 80)
  
- **Erreur (Rouge)** : `#F44336`
  - Usage : Messages d'erreur, alertes, états négatifs
  - RGB : rgb(244, 67, 54)
  
- **Avertissement (Orange)** : `#FF9800`
  - Usage : Avertissements, informations importantes
  - RGB : rgb(255, 152, 0)
  
- **Info (Cyan)** : `#00BCD4`
  - Usage : Messages informatifs
  - RGB : rgb(0, 188, 212)

---

## 📝 Typographie

### Polices
- **Police Principale** : `'Roboto', 'Arial', sans-serif`
- **Police Titres** : `'Roboto', sans-serif` (Bold/Medium)
- **Police Monospace** : `'Roboto Mono', monospace` (pour code/données techniques)

### Hiérarchie des Titres
- **H1** : 
  - Taille : 32px (2rem)
  - Poids : Bold (700)
  - Couleur : `#212121`
  - Espacement : 1.2
  
- **H2** : 
  - Taille : 28px (1.75rem)
  - Poids : Bold (700)
  - Couleur : `#1E88E5`
  - Espacement : 1.3
  
- **H3** : 
  - Taille : 24px (1.5rem)
  - Poids : Medium (500)
  - Couleur : `#212121`
  - Espacement : 1.3
  
- **H4** : 
  - Taille : 20px (1.25rem)
  - Poids : Medium (500)
  - Couleur : `#424242`
  - Espacement : 1.4

### Corps de Texte
- **Texte Principal** :
  - Taille : 16px (1rem)
  - Poids : Regular (400)
  - Couleur : `#212121`
  - Espacement : 1.6
  
- **Texte Secondaire** :
  - Taille : 14px (0.875rem)
  - Poids : Regular (400)
  - Couleur : `#757575`
  - Espacement : 1.5
  
- **Petit Texte** :
  - Taille : 12px (0.75rem)
  - Poids : Regular (400)
  - Couleur : `#9E9E9E`
  - Espacement : 1.4

---

## 🔘 Boutons

### Bouton Principal
```css
background-color: #1E88E5
color: #FFFFFF
border: none
border-radius: 8px
padding: 12px 24px
font-size: 16px
font-weight: 500
box-shadow: 0 2px 4px rgba(30, 136, 229, 0.2)

Hover:
  background-color: #1565C0
  box-shadow: 0 4px 8px rgba(30, 136, 229, 0.3)
```

### Bouton Secondaire
```css
background-color: transparent
color: #1E88E5
border: 2px solid #1E88E5
border-radius: 8px
padding: 10px 22px
font-size: 16px
font-weight: 500

Hover:
  background-color: #E3F2FD
  border-color: #1565C0
  color: #1565C0
```

### Bouton Succès
```css
background-color: #4CAF50
color: #FFFFFF
border: none
border-radius: 8px
padding: 12px 24px

Hover:
  background-color: #388E3C
```

### Bouton Danger
```css
background-color: #F44336
color: #FFFFFF
border: none
border-radius: 8px
padding: 12px 24px

Hover:
  background-color: #D32F2F
```

---

## 📦 Composants

### Cartes (Cards)
```css
background: #FFFFFF
border-radius: 12px
box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08)
padding: 24px
margin-bottom: 20px

Hover:
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.12)
```

### Modales (Popups)
```css
background: #FFFFFF
border-radius: 16px
box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15)
padding: 32px
max-width: 600px
```

### Formulaires

#### Input Text
```css
border: 1px solid #E0E0E0
border-radius: 8px
padding: 12px 16px
font-size: 16px
color: #212121
background: #FFFFFF

Focus:
  border-color: #1E88E5
  box-shadow: 0 0 0 3px rgba(30, 136, 229, 0.1)

Error:
  border-color: #F44336
```

#### Labels
```css
font-size: 14px
font-weight: 500
color: #424242
margin-bottom: 8px
```

### Tableaux
```css
Header:
  background: #E3F2FD
  color: #1565C0
  font-weight: 600
  padding: 16px
  border-bottom: 2px solid #1E88E5

Rows:
  background: #FFFFFF (pair)
  background: #F9F9F9 (impair)
  padding: 14px 16px
  border-bottom: 1px solid #E0E0E0

Hover:
  background: #E3F2FD
```

### Badges
```css
Success:
  background: #4CAF50
  color: #FFFFFF
  padding: 4px 12px
  border-radius: 16px
  font-size: 12px
  font-weight: 500

Warning:
  background: #FF9800
  color: #FFFFFF

Error:
  background: #F44336
  color: #FFFFFF

Info:
  background: #00BCD4
  color: #FFFFFF
```

---

## 🎯 Icônes

### Style
- **Bibliothèque recommandée** : Material Icons ou FontAwesome
- **Taille par défaut** : 24px
- **Couleur par défaut** : `#424242`
- **Couleur active** : `#1E88E5`

### Icônes Principales
- ⏰ Horloge : Pointage, temps
- 👤 Utilisateur : Profil, employé
- 👥 Équipe : Groupes, équipes
- 📊 Graphique : Statistiques, rapports
- ⚙️ Engrenage : Paramètres
- 🔔 Cloche : Notifications
- ✓ Check : Validation, succès
- ✕ Croix : Erreur, fermeture

---

## 📐 Espacements & Layout

### Marges (Margins)
- **xs** : 4px
- **sm** : 8px
- **md** : 16px
- **lg** : 24px
- **xl** : 32px
- **xxl** : 48px

### Paddings
- **xs** : 4px
- **sm** : 8px
- **md** : 16px
- **lg** : 24px
- **xl** : 32px

### Border Radius
- **Petit** : 4px (input, petits éléments)
- **Moyen** : 8px (boutons, cartes simples)
- **Grand** : 12px (cartes importantes)
- **Très grand** : 16px (modales, containers)
- **Rond** : 50% (avatars, badges ronds)

---

## 🌓 Ombres (Shadows)

### Niveaux d'Élévation
```css
Niveau 1 (Cartes au repos):
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.08)

Niveau 2 (Cartes hover):
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.12)

Niveau 3 (Modales):
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.15)

Niveau 4 (Dropdowns, menus):
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.18)
```

---

## 🎬 Animations

### Transitions
```css
Standard:
  transition: all 0.3s ease

Rapide:
  transition: all 0.15s ease

Lente:
  transition: all 0.5s ease
```

### Hover Effects
- **Boutons** : Changement de couleur + légère élévation
- **Cartes** : Augmentation de l'ombre
- **Liens** : Soulignement + changement de couleur

---

## 📱 Responsive Design

### Breakpoints
```css
Mobile: < 768px
Tablet: 768px - 1024px
Desktop: > 1024px
Wide: > 1440px
```

### Adaptations Mobile
- Boutons pleine largeur sur mobile
- Padding réduit (16px au lieu de 24px)
- Taille de police légèrement réduite pour les titres
- Navigation hamburger menu

---

## 🚀 Variables CSS (À implémenter)

```css
:root {
  /* Couleurs Principales */
  --primary-color: #1E88E5;
  --primary-dark: #1565C0;
  --primary-light: #E3F2FD;
  
  /* Couleurs Neutres */
  --white: #FFFFFF;
  --gray-light: #F5F5F5;
  --gray-medium: #9E9E9E;
  --gray-dark: #424242;
  --black: #212121;
  
  /* Couleurs d'État */
  --success: #4CAF50;
  --error: #F44336;
  --warning: #FF9800;
  --info: #00BCD4;
  
  /* Typographie */
  --font-family: 'Roboto', 'Arial', sans-serif;
  --font-size-base: 16px;
  --line-height-base: 1.6;
  
  /* Espacements */
  --spacing-xs: 4px;
  --spacing-sm: 8px;
  --spacing-md: 16px;
  --spacing-lg: 24px;
  --spacing-xl: 32px;
  
  /* Border Radius */
  --radius-sm: 4px;
  --radius-md: 8px;
  --radius-lg: 12px;
  --radius-xl: 16px;
  
  /* Ombres */
  --shadow-sm: 0 2px 4px rgba(0, 0, 0, 0.08);
  --shadow-md: 0 4px 8px rgba(0, 0, 0, 0.12);
  --shadow-lg: 0 8px 16px rgba(0, 0, 0, 0.15);
  
  /* Transitions */
  --transition-fast: 0.15s ease;
  --transition-normal: 0.3s ease;
  --transition-slow: 0.5s ease;
}
```

---

## ✅ Bonnes Pratiques

1. **Cohérence** : Toujours utiliser les couleurs et espacements définis
2. **Accessibilité** : Contraste minimum 4.5:1 pour le texte
3. **Performance** : Optimiser les images et animations
4. **Mobile-first** : Concevoir d'abord pour mobile
5. **Feedback visuel** : Toujours indiquer l'état (hover, active, disabled)

---

*Charte graphique HoraBadge - Version 1.0*
*Basée sur le logo professionnel (Bleu #1E88E5)*
