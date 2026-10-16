from pathlib import Path
import sys

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"comparacion_rostros"))
from entrenar import main

if __name__ == "__main__":
    main("eigenfaces")
