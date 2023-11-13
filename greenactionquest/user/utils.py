# carboncalculator/utils.py
def calculate_carbon(carbon_data):
    travel_emission=calculate_travel_emissions(carbon_data.travel_mode,carbon_data.distance_traveled,carbon_data.fuel_efficiency,carbon_data.number_of_passengers,carbon_data.aircraft_type)
    home_energy_emissions=calculate_home_energy_emissions(carbon_data.electricity_consumption,carbon_data.electricity_source,carbon_data.heating_cooling_energy_consumption,carbon_data.household_size,carbon_data.renewable_energy_capacity)
    waste_emission=calculate_waste_emissions(carbon_data.total_waste_generated,carbon_data.recyclable_materials_recycled,carbon_data.organic_waste_composted)
    dietary_emission=calculate_dietary_emissions(carbon_data.diet_type,carbon_data.food_origin)
    total_emission= travel_emission + home_energy_emissions + waste_emission+dietary_emission
    return round(total_emission, 4)

def calculate_travel_emissions(mode_of_transport, distance_traveled, fuel_efficiency, number_of_passengers=1, aircraft_type=None):
    # Define emission factors (in CO2 per unit) for different modes of travel.
    emission_factors = {
        'car': 2.31,  # Average emission factor for gasoline-powered cars (in kg CO2 per liter).
        'bus': 0.068,  # Emission factor for buses (in kg CO2 per passenger-km).
        'train': 0.041,  # Emission factor for trains (in kg CO2 per passenger-km).
        'domestic_flight': 0.194,  # Emission factor for domestic flights (in kg CO2 per passenger-km).
        'international_flight': 0.193,  # Emission factor for international flights (in kg CO2 per passenger-km).
    }

    # Calculate emissions based on the mode of transportation.
    if mode_of_transport == 'car':
        emissions = (float(distance_traveled) / float(fuel_efficiency)) * emission_factors['car']
    elif mode_of_transport == 'bus':
        emissions = float(distance_traveled) * emission_factors['bus'] / number_of_passengers
    elif mode_of_transport == 'train':
        emissions = float(distance_traveled) * emission_factors['train'] / number_of_passengers
    elif mode_of_transport == 'domestic_flight' or mode_of_transport == 'international_flight':
        emissions = float(distance_traveled) * emission_factors[mode_of_transport]

    # If aircraft type is specified, use a more specific emission factor for flights.
    if mode_of_transport == 'domestic_flight' or mode_of_transport == 'international_flight':
        if aircraft_type:
            specific_emission_factors = {
                'aircraft_type_1': 0.2,  # Emission factor for specific aircraft type 1 (in kg CO2 per passenger-km).
                'aircraft_type_2': 0.18,  # Emission factor for specific aircraft type 2 (in kg CO2 per passenger-km).
                # Add more aircraft types and their emission factors as needed.
            }
            emissions = float(distance_traveled) * specific_emission_factors.get(aircraft_type, emission_factors[mode_of_transport])

    return round(emissions, 4)

def calculate_home_energy_emissions(electricity_consumption, electricity_source, heating_cooling_energy_consumption=0, household_size=1, renewable_energy_capacity=0):
    # Define emission factors (in kg CO2 per kWh) for different electricity sources.
    emission_factors = {
        'coal': 0.95,
        'natural_gas': 0.45,
        'nuclear': 0.01,
        'renewable': 0.0,  # Emission-free sources like solar or wind.
    }

    # Calculate emissions from electricity consumption.
    electricity_emissions = float(electricity_consumption) * emission_factors.get(electricity_source, 0)

    # Calculate emissions from heating and cooling (if applicable).
    heating_cooling_emissions = float(heating_cooling_energy_consumption) * emission_factors.get(electricity_source, 0)

    # Calculate emissions from non-electricity energy consumption.
    non_electricity_emissions = 0  # Add calculations if non-electricity energy sources are used.

    # Calculate emissions from renewable energy offsets (if applicable).
    renewable_energy_emissions = float(-renewable_energy_capacity) * emission_factors['renewable']

    # Calculate total home energy emissions.
    total_emissions = electricity_emissions + heating_cooling_emissions + non_electricity_emissions + renewable_energy_emissions

    # Adjust emissions for household size (per person).
    per_person_emissions = total_emissions / household_size

    return round(total_emissions, 4)

    

def calculate_waste_emissions(total_waste_generated, recyclable_materials_recycled, organic_waste_composted):
    # Define emission factors (in kg CO2 equivalent) for waste disposal methods.
    emission_factors = {
        'landfill': 0.53,  # Emission factor for waste sent to a landfill (in kg CO2 per kg of waste).
        'incineration': 0.85,  # Emission factor for waste incineration (in kg CO2 per kg of waste).
    }

    # Calculate emissions from waste sent to the landfill.
    landfill_emissions = float(total_waste_generated) * emission_factors['landfill']

    # Calculate emissions from waste incineration (if applicable).
    incineration_emissions = 0  # Add calculations if waste is incinerated.

    # Calculate emissions from waste recycling and composting (emission reduction).
    recycling_composting_emissions = -(float(recyclable_materials_recycled) + float(organic_waste_composted)) * emission_factors['landfill']

    # Calculate total waste emissions.
    total_emissions = landfill_emissions + incineration_emissions + recycling_composting_emissions

    return round(total_emissions, 4)

def calculate_dietary_emissions(diet_type,food_origin):
    # Define carbon intensity factors for different food categories (in kg CO2 per kg of food).
    # carbon_intensity_factors = {
    #     'fruits': 0.4,
    #     'vegetables': 0.2,
    #     'grains': 0.3,
    #     'dairy': 2.0,
    #     'meat': 10.0,
    #     'seafood': 7.0,
    # }

    # # Initialize total dietary emissions.
    total_emissions = 0

    # # Calculate emissions based on food consumption.
    # for food, consumption in food_consumption.items():
    #     if food in carbon_intensity_factors:
    #         total_emissions += consumption * carbon_intensity_factors[food]

    # Adjust emissions based on dietary preferences.
    if diet_type == 'vegetarian':
        total_emissions *= 0.5  # A simplified reduction for vegetarian diet.
    elif diet_type == 'vegan':
        total_emissions *= 0.25  # A simplified reduction for vegan diet.

    # Adjust emissions based on food origin (local vs. imported).
    if food_origin == 'local':
        total_emissions *= 0.9  # A simplified reduction for local sourcing.

    return round(total_emissions, 4)

