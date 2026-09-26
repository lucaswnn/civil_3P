from __future__ import annotations

from enum import StrEnum
from math import pi


class PhysicalQuantities(StrEnum):
    LENGTH = "length"
    AREA = "area"
    VOLUME = "volume"
    INERTIA = "inertia"
    FORCE = "force"
    FORCE_PER_LENGTH = "force_per_length"
    MOMENT = "moment"
    MOMENT_PER_LENGTH = "moment_per_length"
    TEMPERATURE = "temperature"
    ANGLE = "angle"
    STRESS = "stress"
    LINEAR_THERMAL_EXPANSION = "linear_thermal_expansion"
    UNITLESS = "unitless"


class LengthUnits(StrEnum):
    METER = "m"
    MILLIMETER = "mm"
    CENTIMETER = "cm"


class AreaUnits(StrEnum):
    SQUARE_METER = "m^2"
    SQUARE_MILLIMETER = "mm^2"
    SQUARE_CENTIMETER = "cm^2"


class VolumeUnits(StrEnum):
    CUBIC_METER = "m^3"
    CUBIC_MILLIMETER = "mm^3"
    CUBIC_CENTIMETER = "cm^3"


class InertiaUnits(StrEnum):
    METER_FOURTH = "m^4"
    MILLIMETER_FOURTH = "mm^4"
    CENTIMETER_FOURTH = "cm^4"


class ForceUnits(StrEnum):
    NEWTON = "N"
    KILONEWTON = "kN"
    TON_FORCE = "tf"
    KILOGRAM_FORCE = "kgf"


class ForcePerLengthUnits(StrEnum):
    NEWTON_PER_METER = "N/m"
    NEWTON_PER_MILLIMETER = "N/mm"
    NEWTON_PER_CENTIMETER = "N/cm"

    KILONEWTON_PER_METER = "kN/m"
    KILONEWTON_PER_MILLIMETER = "kN/mm"
    KILONEWTON_PER_CENTIMETER = "kN/cm"

    TON_FORCE_PER_METER = "tf/m"
    TON_FORCE_PER_MILLIMETER = "tf/mm"
    TON_FORCE_PER_CENTIMETER = "tf/cm"

    KILOGRAM_FORCE_PER_METER = "kgf/m"
    KILOGRAM_FORCE_PER_MILLIMETER = "kgf/mm"
    KILOGRAM_FORCE_PER_CENTIMETER = "kgf/cm"


class MomentUnits(StrEnum):
    NEWTON_METER = "N*m"
    NEWTON_MILLIMETER = "N*mm"
    NEWTON_CENTIMETER = "N*cm"

    KILONEWTON_METER = "kN*m"
    KILONEWTON_MILLIMETER = "kN*mm"
    KILONEWTON_CENTIMETER = "kN*cm"

    TON_FORCE_METER = "tf*m"
    TON_FORCE_MILLIMETER = "tf*mm"
    TON_FORCE_CENTIMETER = "tf*cm"

    KILOGRAM_FORCE_METER = "kgf*m"
    KILOGRAM_FORCE_MILLIMETER = "kgf*mm"
    KILOGRAM_FORCE_CENTIMETER = "kgf*cm"


class MomentPerLengthUnits(StrEnum):
    NEWTON_METER_PER_METER = "N*m/m"
    NEWTON_MILLIMETER_PER_MILLIMETER = "N*mm/mm"
    NEWTON_CENTIMETER_PER_CENTIMETER = "N*cm/cm"

    KILONEWTON_METER_PER_METER = "kN*m/m"
    KILONEWTON_MILLIMETER_PER_MILLIMETER = "kN*mm/mm"
    KILONEWTON_CENTIMETER_PER_CENTIMETER = "kN*cm/cm"

    TON_FORCE_METER_PER_METER = "tf*m/m"
    TON_FORCE_MILLIMETER_PER_MILLIMETER = "tf*mm/mm"
    TON_FORCE_CENTIMETER_PER_CENTIMETER = "tf*cm/cm"

    KILOGRAM_FORCE_METER_PER_METER = "kgf*m/m"
    KILOGRAM_FORCE_MILLIMETER_PER_MILLIMETER = "kgf*mm/mm"
    KILOGRAM_FORCE_CENTIMETER_PER_CENTIMETER = "kgf*cm/cm"


class TemperatureUnits(StrEnum):
    CELSIUS = "C"
    FAHRENHEIT = "F"


class AngleUnits(StrEnum):
    DEGREE = "deg"
    RADIAN = "rad"


class StressUnits(StrEnum):
    NEWTON_PER_SQUARE_METER = "N/m^2"
    NEWTON_PER_SQUARE_MILLIMETER = "N/mm^2"
    NEWTON_PER_SQUARE_CENTIMETER = "N/cm^2"

    KILONEWTON_PER_SQUARE_METER = "kN/m^2"
    KILONEWTON_PER_SQUARE_MILLIMETER = "kN/mm^2"
    KILONEWTON_PER_SQUARE_CENTIMETER = "kN/cm^2"

    TON_FORCE_PER_SQUARE_METER = "tf/m^2"
    TON_FORCE_PER_SQUARE_MILLIMETER = "tf/mm^2"
    TON_FORCE_PER_SQUARE_CENTIMETER = "tf/cm^2"

    KILOGRAM_FORCE_PER_SQUARE_METER = "kgf/m^2"
    KILOGRAM_FORCE_PER_SQUARE_MILLIMETER = "kgf/mm^2"
    KILOGRAM_FORCE_PER_SQUARE_CENTIMETER = "kgf/cm^2"


class LinearThermalExpansionUnits(StrEnum):
    PER_CELSIUS = "1/C"
    PER_FAHRENHEIT = "1/F"


class Unitless(StrEnum):
    UNITLESS = "unitless"
    NONE = "none"


UNITS_SCHEME = {
    PhysicalQuantities.LENGTH: [
        LengthUnits.METER,
        LengthUnits.MILLIMETER,
        LengthUnits.CENTIMETER,
    ],
    PhysicalQuantities.FORCE: [
        ForceUnits.NEWTON,
        ForceUnits.KILONEWTON,
        ForceUnits.TON_FORCE,
        ForceUnits.KILOGRAM_FORCE,
    ],
    PhysicalQuantities.TEMPERATURE: [
        TemperatureUnits.CELSIUS,
        TemperatureUnits.FAHRENHEIT,
    ],
    PhysicalQuantities.FORCE_PER_LENGTH: [
        ForcePerLengthUnits.NEWTON_PER_METER,
        ForcePerLengthUnits.KILONEWTON_PER_METER,
        ForcePerLengthUnits.TON_FORCE_PER_METER,
        ForcePerLengthUnits.KILOGRAM_FORCE_PER_METER,
    ],
    PhysicalQuantities.MOMENT: [
        MomentUnits.NEWTON_METER,
        MomentUnits.KILONEWTON_METER,
        MomentUnits.TON_FORCE_METER,
        MomentUnits.KILOGRAM_FORCE_METER,
    ],
    PhysicalQuantities.MOMENT_PER_LENGTH: [
        MomentPerLengthUnits.NEWTON_METER_PER_METER,
        MomentPerLengthUnits.KILONEWTON_METER_PER_METER,
        MomentPerLengthUnits.TON_FORCE_METER_PER_METER,
        MomentPerLengthUnits.KILOGRAM_FORCE_METER_PER_METER,
    ],
    PhysicalQuantities.UNITLESS: [
        Unitless.UNITLESS,
        Unitless.NONE,
    ],
    PhysicalQuantities.ANGLE: [
        AngleUnits.DEGREE,
        AngleUnits.RADIAN,
    ],
    PhysicalQuantities.AREA: [
        AreaUnits.SQUARE_METER,
        AreaUnits.SQUARE_MILLIMETER,
        AreaUnits.SQUARE_CENTIMETER,
    ],
    PhysicalQuantities.VOLUME: [
        VolumeUnits.CUBIC_METER,
        VolumeUnits.CUBIC_MILLIMETER,
        VolumeUnits.CUBIC_CENTIMETER,
    ],
    PhysicalQuantities.INERTIA: [
        InertiaUnits.METER_FOURTH,
        InertiaUnits.MILLIMETER_FOURTH,
        InertiaUnits.CENTIMETER_FOURTH,
    ],
    PhysicalQuantities.STRESS: [
        StressUnits.NEWTON_PER_SQUARE_METER,
        StressUnits.NEWTON_PER_SQUARE_MILLIMETER,
        StressUnits.NEWTON_PER_SQUARE_CENTIMETER,
        StressUnits.KILONEWTON_PER_SQUARE_METER,
        StressUnits.KILONEWTON_PER_SQUARE_MILLIMETER,
        StressUnits.KILONEWTON_PER_SQUARE_CENTIMETER,
        StressUnits.TON_FORCE_PER_SQUARE_METER,
        StressUnits.TON_FORCE_PER_SQUARE_MILLIMETER,
        StressUnits.TON_FORCE_PER_SQUARE_CENTIMETER,
        StressUnits.KILOGRAM_FORCE_PER_SQUARE_METER,
        StressUnits.KILOGRAM_FORCE_PER_SQUARE_MILLIMETER,
        StressUnits.KILOGRAM_FORCE_PER_SQUARE_CENTIMETER,
    ],
    PhysicalQuantities.LINEAR_THERMAL_EXPANSION: [
        LinearThermalExpansionUnits.PER_CELSIUS,
        LinearThermalExpansionUnits.PER_FAHRENHEIT,
    ],
}

DEFAULT_UNITS = {
    PhysicalQuantities.LENGTH: LengthUnits.METER,
    PhysicalQuantities.FORCE: ForceUnits.TON_FORCE,
    PhysicalQuantities.TEMPERATURE: TemperatureUnits.CELSIUS,
    PhysicalQuantities.FORCE_PER_LENGTH: ForcePerLengthUnits.TON_FORCE_PER_METER,
    PhysicalQuantities.MOMENT: MomentUnits.TON_FORCE_METER,
    PhysicalQuantities.MOMENT_PER_LENGTH: MomentPerLengthUnits.TON_FORCE_METER_PER_METER,
    PhysicalQuantities.UNITLESS: Unitless.UNITLESS,
    PhysicalQuantities.ANGLE: AngleUnits.RADIAN,
    PhysicalQuantities.AREA: AreaUnits.SQUARE_METER,
    PhysicalQuantities.VOLUME: VolumeUnits.CUBIC_METER,
    PhysicalQuantities.INERTIA: InertiaUnits.METER_FOURTH,
    PhysicalQuantities.STRESS: StressUnits.NEWTON_PER_SQUARE_METER,
    PhysicalQuantities.LINEAR_THERMAL_EXPANSION: LinearThermalExpansionUnits.PER_CELSIUS,
}
