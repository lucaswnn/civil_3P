from __future__ import annotations

from math import pi
from typing import TYPE_CHECKING

from civil_3P.standard.units import (
    AngleUnits,
    AreaUnits,
    ForcePerLengthUnits,
    ForceUnits,
    InertiaUnits,
    LengthUnits,
    LinearThermalExpansionUnits,
    PhysicalQuantities,
    MomentPerLengthUnits,
    MomentUnits,
    TemperatureUnits,
    StressUnits,
    Unitless,
    VolumeUnits,
)

if TYPE_CHECKING:
    from enum import StrEnum


class UnitConverter:
    @staticmethod
    def get_physical_quantity(unit: StrEnum) -> PhysicalQuantities:
        if isinstance(unit, LengthUnits):
            return PhysicalQuantities.LENGTH
        elif isinstance(unit, ForceUnits):
            return PhysicalQuantities.FORCE
        elif isinstance(unit, ForcePerLengthUnits):
            return PhysicalQuantities.FORCE_PER_LENGTH
        elif isinstance(unit, MomentUnits):
            return PhysicalQuantities.MOMENT
        elif isinstance(unit, MomentPerLengthUnits):
            return PhysicalQuantities.MOMENT_PER_LENGTH
        elif isinstance(unit, TemperatureUnits):
            return PhysicalQuantities.TEMPERATURE
        elif isinstance(unit, LinearThermalExpansionUnits):
            return PhysicalQuantities.LINEAR_THERMAL_EXPANSION
        elif isinstance(unit, AngleUnits):
            return PhysicalQuantities.ANGLE
        elif isinstance(unit, AreaUnits):
            return PhysicalQuantities.AREA
        elif isinstance(unit, VolumeUnits):
            return PhysicalQuantities.VOLUME
        elif isinstance(unit, InertiaUnits):
            return PhysicalQuantities.INERTIA
        elif isinstance(unit, StressUnits):
            return PhysicalQuantities.STRESS
        elif isinstance(unit, Unitless):
            return PhysicalQuantities.UNITLESS
        else:
            raise ValueError(f"Unsupported unit: {unit}")

    @staticmethod
    def convert(value: float, from_unit: StrEnum, to_unit: StrEnum) -> float:
        if isinstance(from_unit, LengthUnits) and isinstance(to_unit, LengthUnits):
            return UnitConverter.convert_length(value, from_unit, to_unit)
        elif isinstance(from_unit, ForceUnits) and isinstance(to_unit, ForceUnits):
            return UnitConverter.convert_force(value, from_unit, to_unit)
        elif isinstance(from_unit, TemperatureUnits) and isinstance(to_unit, TemperatureUnits):
            return UnitConverter.convert_temperature(value, from_unit, to_unit)
        elif isinstance(from_unit, MomentUnits) and isinstance(to_unit, MomentUnits):
            return UnitConverter.convert_moment(value, from_unit, to_unit)
        elif isinstance(from_unit, MomentPerLengthUnits) and isinstance(to_unit, MomentPerLengthUnits):
            return UnitConverter.convert_moment_per_length(value, from_unit, to_unit)
        elif isinstance(from_unit, ForcePerLengthUnits) and isinstance(to_unit, ForcePerLengthUnits):
            return UnitConverter.convert_force_per_length(value, from_unit, to_unit)
        elif isinstance(from_unit, AngleUnits) and isinstance(to_unit, AngleUnits):
            return UnitConverter.convert_angle(value, from_unit, to_unit)
        elif isinstance(from_unit, AreaUnits) and isinstance(to_unit, AreaUnits):
            return UnitConverter.convert_area(value, from_unit, to_unit)
        elif isinstance(from_unit, VolumeUnits) and isinstance(to_unit, VolumeUnits):
            return UnitConverter.convert_volume(value, from_unit, to_unit)
        elif isinstance(from_unit, InertiaUnits) and isinstance(to_unit, InertiaUnits):
            return UnitConverter.convert_inertia(value, from_unit, to_unit)
        elif isinstance(from_unit, StressUnits) and isinstance(to_unit, StressUnits):
            return UnitConverter.convert_stress(value, from_unit, to_unit)
        elif isinstance(from_unit, LinearThermalExpansionUnits) and isinstance(to_unit, LinearThermalExpansionUnits):
            return UnitConverter.convert_linear_thermal_expansion(value, from_unit, to_unit)
        else:
            raise ValueError(
                f"Unsupported unit conversion from {from_unit} to {to_unit}")

    @staticmethod
    def convert_length(value: float, from_unit: LengthUnits, to_unit: LengthUnits) -> float:
        conversion_factors = {
            LengthUnits.METER: 1.0,
            LengthUnits.MILLIMETER: 1000.0,
            LengthUnits.CENTIMETER: 100.0,
        }
        return value * (conversion_factors[to_unit] / conversion_factors[from_unit])

    @staticmethod
    def convert_area(value: float, from_unit: AreaUnits, to_unit: AreaUnits) -> float:
        conversion_factors = {
            AreaUnits.SQUARE_METER: 1.0,
            AreaUnits.SQUARE_MILLIMETER: 1000000.0,
            AreaUnits.SQUARE_CENTIMETER: 10000.0,
        }
        return value * (conversion_factors[to_unit] / conversion_factors[from_unit])

    @staticmethod
    def convert_volume(value: float, from_unit: VolumeUnits, to_unit: VolumeUnits) -> float:
        conversion_factors = {
            VolumeUnits.CUBIC_METER: 1.0,
            VolumeUnits.CUBIC_MILLIMETER: 1e9,
            VolumeUnits.CUBIC_CENTIMETER: 1e6,
        }
        return value * (conversion_factors[to_unit] / conversion_factors[from_unit])

    @staticmethod
    def convert_inertia(value: float, from_unit: InertiaUnits, to_unit: InertiaUnits) -> float:
        conversion_factors = {
            InertiaUnits.METER_FOURTH: 1.0,
            InertiaUnits.MILLIMETER_FOURTH: 1e12,
            InertiaUnits.CENTIMETER_FOURTH: 1e8,
        }
        return value * (conversion_factors[to_unit] / conversion_factors[from_unit])

    @staticmethod
    def convert_force(value: float, from_unit: ForceUnits, to_unit: ForceUnits) -> float:
        conversion_factors = {
            ForceUnits.NEWTON: 1.0,
            ForceUnits.KILONEWTON: 1000.0,
            ForceUnits.TON_FORCE: 9806.65,
            ForceUnits.KILOGRAM_FORCE: 9.80665,
        }
        return value * (conversion_factors[to_unit] / conversion_factors[from_unit])

    @staticmethod
    def convert_temperature(value: float, from_unit: TemperatureUnits, to_unit: TemperatureUnits) -> float:
        if from_unit == to_unit:
            return value
        if from_unit == TemperatureUnits.CELSIUS and to_unit == TemperatureUnits.FAHRENHEIT:
            return (value * 9/5) + 32
        if from_unit == TemperatureUnits.FAHRENHEIT and to_unit == TemperatureUnits.CELSIUS:
            return (value - 32) * 5/9
        raise ValueError(
            f"Unsupported temperature conversion from {from_unit} to {to_unit}")

    @staticmethod
    def convert_moment(value: float, from_unit: MomentUnits, to_unit: MomentUnits) -> float:
        conversion_factors = {
            MomentUnits.NEWTON_METER: 1.0,
            MomentUnits.NEWTON_MILLIMETER: 1000.0,
            MomentUnits.NEWTON_CENTIMETER: 100.0,
            MomentUnits.KILONEWTON_METER: 1000.0,
            MomentUnits.KILONEWTON_MILLIMETER: 1000000.0,
            MomentUnits.KILONEWTON_CENTIMETER: 100000.0,
            MomentUnits.TON_FORCE_METER: 9806.65,
            MomentUnits.TON_FORCE_MILLIMETER: 9806650.0,
            MomentUnits.TON_FORCE_CENTIMETER: 980665.0,
            MomentUnits.KILOGRAM_FORCE_METER: 9.80665,
            MomentUnits.KILOGRAM_FORCE_MILLIMETER: 9806.65,
            MomentUnits.KILOGRAM_FORCE_CENTIMETER: 980.665,
        }
        return value * (conversion_factors[to_unit] / conversion_factors[from_unit])

    @staticmethod
    def convert_moment_per_length(value: float, from_unit: MomentPerLengthUnits, to_unit: MomentPerLengthUnits) -> float:
        conversion_factors = {
            MomentPerLengthUnits.NEWTON_METER_PER_METER: 1.0,
            MomentPerLengthUnits.NEWTON_MILLIMETER_PER_MILLIMETER: 1000.0,
            MomentPerLengthUnits.NEWTON_CENTIMETER_PER_CENTIMETER: 100.0,
            MomentPerLengthUnits.KILONEWTON_METER_PER_METER: 1000.0,
            MomentPerLengthUnits.KILONEWTON_MILLIMETER_PER_MILLIMETER: 1000000.0,
            MomentPerLengthUnits.KILONEWTON_CENTIMETER_PER_CENTIMETER: 100000.0,
            MomentPerLengthUnits.TON_FORCE_METER_PER_METER: 9806.65,
            MomentPerLengthUnits.TON_FORCE_MILLIMETER_PER_MILLIMETER: 9806650.0,
            MomentPerLengthUnits.TON_FORCE_CENTIMETER_PER_CENTIMETER: 980665.0,
            MomentPerLengthUnits.KILOGRAM_FORCE_METER_PER_METER: 9.80665,
            MomentPerLengthUnits.KILOGRAM_FORCE_MILLIMETER_PER_MILLIMETER: 9806.65,
            MomentPerLengthUnits.KILOGRAM_FORCE_CENTIMETER_PER_CENTIMETER: 980.665,
        }
        return value * (conversion_factors[to_unit] / conversion_factors[from_unit])

    @staticmethod
    def convert_force_per_length(value: float, from_unit: ForcePerLengthUnits, to_unit: ForcePerLengthUnits) -> float:
        conversion_factors = {
            ForcePerLengthUnits.NEWTON_PER_METER: 1.0,
            ForcePerLengthUnits.NEWTON_PER_MILLIMETER: 1000.0,
            ForcePerLengthUnits.NEWTON_PER_CENTIMETER: 100.0,
            ForcePerLengthUnits.KILONEWTON_PER_METER: 1000.0,
            ForcePerLengthUnits.KILONEWTON_PER_MILLIMETER: 1000000.0,
            ForcePerLengthUnits.KILONEWTON_PER_CENTIMETER: 100000.0,
            ForcePerLengthUnits.TON_FORCE_PER_METER: 9806.65,
            ForcePerLengthUnits.TON_FORCE_PER_MILLIMETER: 9806650.0,
            ForcePerLengthUnits.TON_FORCE_PER_CENTIMETER: 980665.0,
            ForcePerLengthUnits.KILOGRAM_FORCE_PER_METER: 9.80665,
            ForcePerLengthUnits.KILOGRAM_FORCE_PER_MILLIMETER: 9806.65,
            ForcePerLengthUnits.KILOGRAM_FORCE_PER_CENTIMETER: 980.665,
        }
        return value * (conversion_factors[to_unit] / conversion_factors[from_unit])

    @staticmethod
    def convert_angle(value: float, from_unit: AngleUnits, to_unit: AngleUnits) -> float:
        if from_unit == to_unit:
            return value
        if from_unit == AngleUnits.DEGREE and to_unit == AngleUnits.RADIAN:
            return value * (pi / 180.0)
        if from_unit == AngleUnits.RADIAN and to_unit == AngleUnits.DEGREE:
            return value * (180.0 / pi)
        raise ValueError(
            f"Unsupported angle conversion from {from_unit} to {to_unit}")

    def convert_stress(value: float, from_unit: StressUnits, to_unit: StressUnits) -> float:
        conversion_factors = {
            StressUnits.NEWTON_PER_SQUARE_METER: 1.0,
            StressUnits.NEWTON_PER_SQUARE_MILLIMETER: 1e6,
            StressUnits.NEWTON_PER_SQUARE_CENTIMETER: 1e4,
            StressUnits.KILONEWTON_PER_SQUARE_METER: 1000.0,
            StressUnits.KILONEWTON_PER_SQUARE_MILLIMETER: 1e9,
            StressUnits.KILONEWTON_PER_SQUARE_CENTIMETER: 1e7,
            StressUnits.TON_FORCE_PER_SQUARE_METER: 9806.65,
            StressUnits.TON_FORCE_PER_SQUARE_MILLIMETER: 9.80665e9,
            StressUnits.TON_FORCE_PER_SQUARE_CENTIMETER: 9.80665e7,
            StressUnits.KILOGRAM_FORCE_PER_SQUARE_METER: 9.80665,
            StressUnits.KILOGRAM_FORCE_PER_SQUARE_MILLIMETER: 9.80665e6,
            StressUnits.KILOGRAM_FORCE_PER_SQUARE_CENTIMETER: 9.80665e4,
        }
        return value * (conversion_factors[to_unit] / conversion_factors[from_unit])

    @staticmethod
    def convert_linear_thermal_expansion(value: float, from_unit: LinearThermalExpansionUnits, to_unit: LinearThermalExpansionUnits) -> float:
        if from_unit == to_unit:
            return value
        if from_unit == LinearThermalExpansionUnits.PER_CELSIUS and to_unit == LinearThermalExpansionUnits.PER_FAHRENHEIT:
            return value * (9/5)
        if from_unit == LinearThermalExpansionUnits.PER_FAHRENHEIT and to_unit == LinearThermalExpansionUnits.PER_CELSIUS:
            return value * (5/9)
        raise ValueError(
            f"Unsupported linear thermal expansion conversion from {from_unit} to {to_unit}")
