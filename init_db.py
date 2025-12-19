from app.database import Base, engine
from app.models import *

Base.metadata.create_all(bind=engine)

print("Toutes les tables ont été créées avec succès.")
print("")
print("Tables disponibles :")
print(" - vehicules")
print(" - entretiens")
print(" - reparations")
print(" - affectations")
print(" - alertes")
print("")
print("Tu peux maintenant :")
print(" lancer : sqlite3 parc_automobile.db")
print(" taper : python -c 'from init_db import *' ")
print("")
print("Prochaine etape : Go test en vrai")