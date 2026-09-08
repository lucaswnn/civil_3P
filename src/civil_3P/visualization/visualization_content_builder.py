class ResultVisualizationBuilder:
    def __init__(
        self,
        mode: Visualization2DMode,
        component: mc.ModelComponents,
    ) -> None:
        self._mode = mode
        self._component = component

    def build(self, results: ResultData) -> ResultVisualizationData:
        if self._component == mc.ModelComponents.NODES:
            return self._build_node_points(results)

        if self._component == mc.ModelComponents.ELEMENTS_1D:
            return self._build_element_1d_profile(results)

        if self._component == mc.ModelComponents.ELEMENTS_2D:
            if self._mode == Visualization2DMode.ELEMENT:
                return self._build_element_2d_uniform(results)
            if self._mode == Visualization2DMode.NODE_AVERAGED:
                return self._build_element_2d_shared_nodes(results)
            if self._mode == Visualization2DMode.NODE_RAW:
                return self._build_element_2d_isolated_nodes(results)

        raise ValueError(
            f"Unsupported combination of component {self._component!r} "
            f"and mode {self._mode!r}"
        )

    def _require_columns(self, results: pd.DataFrame, columns: tuple[str, ...]) -> None:
        missing = [column for column in columns if column not in results.columns]
        if missing:
            raise ValueError(
                f"Missing expected columns {missing} for component "
                f"{self._component!r} and mode {self._mode!r}"
            )

    def _value_range(self, values: pd.Series) -> tuple[float, float]:
        if values.empty:
            return (0.0, 0.0)
        return (float(values.min()), float(values.max()))

    def _build_node_points(self, results: ResultData) -> ResultVisualizationData:
        self._require_columns(
            results.result_df,
            (
                rpr.TaskNodeResultsColumns.NODE,
                rpr.TaskNodeResultsColumns.VALUE,
            ),
        )

        node_values = {
            str(node_id): float(value)
            for node_id, value in zip(results.result_df[rpr.TaskNodeResultsColumns.NODE], results.result_df[rpr.TaskNodeResultsColumns.VALUE])
        }

        return ResultVisualizationData(
            kind=VisualizationContentKind.NODE_POINTS,
            elements=results.elements,
            nodes=results.nodes,
            value_range=self._value_range(
                results.result_df[rpr.TaskNodeResultsColumns.VALUE]),
            node_values=node_values,
        )

    def _build_element_1d_profile(self, results: ResultData) -> ResultVisualizationData:
        self._require_columns(
            results.result_df,
            (
                rpr.Task1DResultsColumns.ELEMENT,
                rpr.Task1DResultsColumns.STATION,
                rpr.Task1DResultsColumns.VALUE,
            ),
        )

        element_station_values: dict[str, list[tuple[float, float]]] = {}
        grouped = results.result_df.groupby(rpr.Task1DResultsColumns.ELEMENT)
        for element_id, group in grouped:
            ordered = group.sort_values(rpr.Task1DResultsColumns.STATION)
            element_station_values[str(element_id)] = list(
                zip(
                    ordered[rpr.Task1DResultsColumns.STATION].astype(float),
                    ordered[rpr.Task1DResultsColumns.VALUE].astype(float),
                )
            )

        return ResultVisualizationData(
            kind=VisualizationContentKind.ELEMENT_1D_PROFILE,
            elements=results.elements,
            nodes=results.nodes,
            value_range=self._value_range(
                results.result_df[rpr.Task1DResultsColumns.VALUE]),
            element_station_values=element_station_values,
        )

    def _build_element_2d_uniform(self, results: ResultData) -> ResultVisualizationData:
        self._require_columns(
            results.result_df,
            (
                rpr.Task2DResultsColumns.ELEMENT,
                rpr.Task2DResultsColumns.VALUE,
            ),
        )

        element_values = {
            str(element_id): float(value)
            for element_id, value in zip(
                results.result_df[rpr.Task2DResultsColumns.ELEMENT], results.result_df[rpr.Task2DResultsColumns.VALUE]
            )
        }

        return ResultVisualizationData(
            kind=VisualizationContentKind.ELEMENT_2D_UNIFORM,
            elements=results.elements,
            nodes=results.nodes,
            value_range=self._value_range(
                results.result_df[rpr.Task2DResultsColumns.VALUE]),
            element_values=element_values,
        )

    def _build_element_2d_shared_nodes(
        self, results: ResultData
    ) -> ResultVisualizationData:
        self._require_columns(
            results.result_df,
            (
                rpr.Task2DResultsColumns.NODE,
                rpr.Task2DResultsColumns.VALUE,
            ),
        )

        node_values = {
            str(node_id): float(value)
            for node_id, value in zip(
                results.result_df[rpr.Task2DResultsColumns.NODE], results.result_df[rpr.Task2DResultsColumns.VALUE]
            )
        }

        return ResultVisualizationData(
            kind=VisualizationContentKind.ELEMENT_2D_SHARED_NODES,
            elements=results.elements,
            nodes=results.nodes,
            value_range=self._value_range(
                results.result_df[rpr.Task2DResultsColumns.VALUE]),
            element_node_values=node_values,
        )

    def _build_element_2d_isolated_nodes(
        self, results: ResultData
    ) -> ResultVisualizationData:
        self._require_columns(
            results.result_df,
            (
                rpr.Task2DResultsColumns.ELEMENT,
                rpr.Task2DResultsColumns.NODE,
                rpr.Task2DResultsColumns.VALUE,
            ),
        )

        element_node_values: dict[str, dict[str, float]] = {}
        grouped = results.result_df.groupby(rpr.Task2DResultsColumns.ELEMENT)
        for element_id, group in grouped:
            element_node_values[str(element_id)] = {
                str(node_id): float(value)
                for node_id, value in zip(
                    group[rpr.Task2DResultsColumns.NODE], group[rpr.Task2DResultsColumns.VALUE]
                )
            }

        return ResultVisualizationData(
            kind=VisualizationContentKind.ELEMENT_2D_ISOLATED_NODES,
            elements=results.elements,
            nodes=results.nodes,
            value_range=self._value_range(
                results.result_df[rpr.Task2DResultsColumns.VALUE]),
            element_node_values=element_node_values,
        )
