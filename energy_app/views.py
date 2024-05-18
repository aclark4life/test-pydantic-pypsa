# Create your views here.

from ninja import NinjaAPI
from pydantic import BaseModel, Field, validator
import pypsa

api = NinjaAPI()


class EnergyData(BaseModel):
    name: str
    capacity_mw: float = Field(..., gt=0, description="Capacity in megawatts")
    efficiency: float = Field(
        ..., gt=0, le=1, description="Efficiency as a decimal between 0 and 1"
    )
    cost_per_mw: float = Field(..., gt=0, description="Cost per megawatt in USD")

    @validator("name")
    def name_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError("Name must not be empty")
        return v


@api.post("/add-energy-system/")
def add_energy_system(request, data: EnergyData):
    try:
        network = pypsa.Network()
        network.add(
            "Generator",
            data.name,
            p_nom_extendable=True,
            p_nom=data.capacity_mw,
            efficiency=data.efficiency,
            capital_cost=data.cost_per_mw,
        )
        return {"message": "Energy system added successfully", "data": data.dict()}
    except Exception as e:
        return {"detail": str(e)}


@api.get("/")
def read_root(request):
    return {"message": "Welcome to the Energy Management API"}
