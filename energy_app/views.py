# Create your views here.
from ninja import NinjaAPI
from pydantic import BaseModel, Field, validator
from typing import List
import pypsa
from faker import Faker
from .models import EnergySystem

api = NinjaAPI()
faker = Faker()

class EnergyData(BaseModel):
    name: str
    capacity_mw: float = Field(..., gt=0, description="Capacity in megawatts")
    efficiency: float = Field(..., gt=0, le=1, description="Efficiency as a decimal between 0 and 1")
    cost_per_mw: float = Field(..., gt=0, description="Cost per megawatt in USD")

    @validator('name')
    def name_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('Name must not be empty')
        return v

@api.post("/add-energy-system/")
def add_energy_system(request, data: EnergyData):
    try:
        network = pypsa.Network()
        network.add("Generator", data.name,
                    p_nom_extendable=True,
                    p_nom=data.capacity_mw,
                    efficiency=data.efficiency,
                    capital_cost=data.cost_per_mw)
        # Save to the database
        EnergySystem.objects.create(
            name=data.name,
            capacity_mw=data.capacity_mw,
            efficiency=data.efficiency,
            cost_per_mw=data.cost_per_mw
        )
        return {"message": "Energy system added successfully", "data": data.dict()}
    except Exception as e:
        return {"detail": str(e)}

@api.post("/add-test-energy-systems/")
def add_test_energy_systems(request, count: int = 10):
    try:
        for _ in range(count):
            name = faker.company()
            capacity_mw = faker.random_number(digits=3)
            efficiency = faker.random.uniform(0.5, 1.0)
            cost_per_mw = faker.random_number(digits=5)

            # Save to the database
            EnergySystem.objects.create(
                name=name,
                capacity_mw=capacity_mw,
                efficiency=efficiency,
                cost_per_mw=cost_per_mw
            )
        return {"message": f"Added {count} test energy systems successfully."}
    except Exception as e:
        return {"detail": str(e)}


@api.get("/energy-systems/", response=List[EnergyData])
def list_energy_systems(request):
    energy_systems = EnergySystem.objects.all()
    return [EnergyData(
        name=system.name,
        capacity_mw=system.capacity_mw,
        efficiency=system.efficiency,
        cost_per_mw=system.cost_per_mw
    ) for system in energy_systems]


@api.get("/")
def read_root(request):
    return {"message": "Welcome to the Energy Management API"}
