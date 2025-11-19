#!/bin/bash
# 🚀 Commandes Utiles - Page Employé
# Utilisation: source utilisé-commandes.sh

PROJECT_PATH="/home/keirs/epitech/Projet_HoraBadge"

# 🎨 Couleurs
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}🚀 Page Employé - Commandes Utiles${NC}"
echo -e "${BLUE}========================================${NC}\n"

# ==========================================
# 1. DÉMARRAGE
# ==========================================
start_project() {
    echo -e "${YELLOW}▶ Démarrage du projet...${NC}"
    cd "$PROJECT_PATH"
    sudo docker-compose up -d
    echo -e "${GREEN}✓ Projet démarré${NC}"
    echo -e "${GREEN}Frontend: http://localhost:5173${NC}"
    echo -e "${GREEN}Backend: http://localhost:8000${NC}"
}

# ==========================================
# 2. ARRÊT
# ==========================================
stop_project() {
    echo -e "${YELLOW}⏹ Arrêt du projet...${NC}"
    cd "$PROJECT_PATH"
    sudo docker-compose down
    echo -e "${GREEN}✓ Projet arrêté${NC}"
}

# ==========================================
# 3. REDÉMARRAGE BACKEND
# ==========================================
restart_backend() {
    echo -e "${YELLOW}🔄 Redémarrage du backend...${NC}"
    cd "$PROJECT_PATH"
    sudo docker-compose restart backend
    echo -e "${GREEN}✓ Backend redémarré${NC}"
    echo -e "${BLUE}Accès: http://localhost:8000${NC}"
}

# ==========================================
# 4. LOGS BACKEND
# ==========================================
logs_backend() {
    echo -e "${YELLOW}📋 Logs du backend${NC}"
    cd "$PROJECT_PATH"
    sudo docker-compose logs backend -f
}

# ==========================================
# 5. LOGS BDD
# ==========================================
logs_db() {
    echo -e "${YELLOW}📋 Logs de la base de données${NC}"
    cd "$PROJECT_PATH"
    sudo docker-compose logs db -f
}

# ==========================================
# 6. STATUS SERVICES
# ==========================================
status_services() {
    echo -e "${YELLOW}📊 État des services${NC}"
    cd "$PROJECT_PATH"
    sudo docker-compose ps
}

# ==========================================
# 7. ACCÈS BDD
# ==========================================
access_db() {
    echo -e "${YELLOW}🔓 Connexion à la base de données${NC}"
    cd "$PROJECT_PATH"
    sudo docker exec -it projet_horabadge_db_1 psql -U postgres -d myapp_db
}

# ==========================================
# 8. TEST API POINTAGES
# ==========================================
test_api_checkin() {
    echo -e "${YELLOW}🧪 Test CHECK-IN${NC}"
    curl -X POST http://localhost:8000/api/attendance/check-in/ \
      -H "Authorization: Token YOUR_TOKEN" \
      -H "Content-Type: application/json"
    echo -e "\n${GREEN}✓ Test complété${NC}"
}

test_api_checkout() {
    echo -e "${YELLOW}🧪 Test CHECK-OUT${NC}"
    curl -X POST http://localhost:8000/api/attendance/check-out/ \
      -H "Authorization: Token YOUR_TOKEN" \
      -H "Content-Type: application/json"
    echo -e "\n${GREEN}✓ Test complété${NC}"
}

test_api_anomalies() {
    echo -e "${YELLOW}🧪 Test ANOMALIES${NC}"
    curl -X GET http://localhost:8000/api/attendance/anomalies/ \
      -H "Authorization: Token YOUR_TOKEN"
    echo -e "\n${GREEN}✓ Test complété${NC}"
}

test_api_calendar() {
    echo -e "${YELLOW}🧪 Test CALENDRIER${NC}"
    curl -X GET http://localhost:8000/api/attendance/calendar/ \
      -H "Authorization: Token YOUR_TOKEN"
    echo -e "\n${GREEN}✓ Test complété${NC}"
}

# ==========================================
# 9. VÉRIFICATIONS BDD
# ==========================================
check_attendances() {
    echo -e "${YELLOW}🔍 Pointages d'aujourd'hui${NC}"
    cd "$PROJECT_PATH"
    sudo docker exec -e PGPASSWORD=postgres projet_horabadge_db_1 psql -U postgres -d myapp_db -c "SELECT id, user_id, attendance_type, timestamp FROM attendances WHERE date = CURRENT_DATE ORDER BY timestamp DESC;"
}

check_teams() {
    echo -e "${YELLOW}🔍 Équipes et membres${NC}"
    cd "$PROJECT_PATH"
    sudo docker exec -e PGPASSWORD=postgres projet_horabadge_db_1 psql -U postgres -d myapp_db -c "SELECT t.id, t.name, COUNT(tm.user_id) as members FROM teams t LEFT JOIN teams_members tm ON t.id = tm.team_id GROUP BY t.id, t.name;"
}

check_users() {
    echo -e "${YELLOW}🔍 Utilisateurs${NC}"
    cd "$PROJECT_PATH"
    sudo docker exec -e PGPASSWORD=postgres projet_horabadge_db_1 psql -U postgres -d myapp_db -c "SELECT id, username, first_name, last_name, role, email FROM users;"
}

# ==========================================
# 10. AIDE
# ==========================================
show_help() {
    echo -e "${BLUE}Commandes disponibles:${NC}\n"
    echo -e "${GREEN}Démarrage & Arrêt:${NC}"
    echo "  start_project        - Démarrer le projet"
    echo "  stop_project         - Arrêter le projet"
    echo "  restart_backend      - Redémarrer le backend"
    echo ""
    echo -e "${GREEN}Logs & Monitoring:${NC}"
    echo "  logs_backend         - Afficher les logs du backend"
    echo "  logs_db              - Afficher les logs de la BDD"
    echo "  status_services      - État des services"
    echo ""
    echo -e "${GREEN}Base de Données:${NC}"
    echo "  access_db            - Accéder à la BDD (psql)"
    echo "  check_attendances    - Voir les pointages du jour"
    echo "  check_teams          - Voir les équipes"
    echo "  check_users          - Voir les utilisateurs"
    echo ""
    echo -e "${GREEN}Tests API:${NC}"
    echo "  test_api_checkin     - Tester endpoint check-in"
    echo "  test_api_checkout    - Tester endpoint check-out"
    echo "  test_api_anomalies   - Tester endpoint anomalies"
    echo "  test_api_calendar    - Tester endpoint calendrier"
    echo ""
    echo -e "${GREEN}Autres:${NC}"
    echo "  show_help            - Afficher cette aide"
    echo ""
    echo -e "${BLUE}Exemple: start_project${NC}"
}

# ==========================================
# 11. MENU PRINCIPAL
# ==========================================
main_menu() {
    while true; do
        echo ""
        echo -e "${BLUE}========================================${NC}"
        echo -e "${BLUE}Page Employé - Menu Principal${NC}"
        echo -e "${BLUE}========================================${NC}"
        echo ""
        echo "1. Démarrer le projet"
        echo "2. Arrêter le projet"
        echo "3. Redémarrer le backend"
        echo "4. Afficher logs backend"
        echo "5. Afficher logs BDD"
        echo "6. État des services"
        echo "7. Accéder à la BDD"
        echo "8. Vérifier les pointages"
        echo "9. Vérifier les équipes"
        echo "10. Vérifier les utilisateurs"
        echo "11. Afficher l'aide"
        echo "0. Quitter"
        echo ""
        read -p "Choisir une option (0-11): " choice
        
        case $choice in
            1) start_project ;;
            2) stop_project ;;
            3) restart_backend ;;
            4) logs_backend ;;
            5) logs_db ;;
            6) status_services ;;
            7) access_db ;;
            8) check_attendances ;;
            9) check_teams ;;
            10) check_users ;;
            11) show_help ;;
            0) echo -e "${GREEN}Au revoir!${NC}"; exit 0 ;;
            *) echo -e "${RED}❌ Option invalide${NC}" ;;
        esac
    done
}

# ==========================================
# LANCEMENT
# ==========================================
if [ $# -eq 0 ]; then
    show_help
else
    case "$1" in
        start) start_project ;;
        stop) stop_project ;;
        restart) restart_backend ;;
        logs-backend) logs_backend ;;
        logs-db) logs_db ;;
        status) status_services ;;
        db) access_db ;;
        check-attendance) check_attendances ;;
        check-teams) check_teams ;;
        check-users) check_users ;;
        test-checkin) test_api_checkin ;;
        test-checkout) test_api_checkout ;;
        test-anomalies) test_api_anomalies ;;
        test-calendar) test_api_calendar ;;
        menu) main_menu ;;
        help) show_help ;;
        *) 
            echo -e "${RED}❌ Commande inconnue: $1${NC}"
            show_help
            ;;
    esac
fi
