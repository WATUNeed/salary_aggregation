from src.domain.abc.dal import DocumentDAO
from src.domain.payment.dto import PaymentCreateDTO, PaymentUpdateDTO, PaymentGroupEnum, SumPeriodAggregationOutputDTO
from src.domain.payment.model import Payment
from src.domain.payment.service import GroupStrategySelector
from src.domain.period.dto import PeriodDTO


class PaymentDAO(DocumentDAO[Payment, PaymentCreateDTO, PaymentUpdateDTO]):
    document = Payment
    create_dto = PaymentCreateDTO
    update_dto = PaymentUpdateDTO

    async def get_sum_for_period_by_group_type(
            self, period: PeriodDTO, group_type: PaymentGroupEnum
    ) -> SumPeriodAggregationOutputDTO:
        group_selector = GroupStrategySelector(group_type)

        pipeline = [
            {
                "$match": {
                    "dt": {
                        "$gte": period.from_dt, "$lt": period.to_dt
                    }
                }
            },
            {
                "$group": {
                    "_id": group_selector.group_expression,
                    "total": {
                        "$sum": "$value"
                    }
                }
            },
            {
                "$sort": group_selector.sort_keys
            }
        ]

        results = await self.document.aggregate(pipeline).to_list(length=None)

        return SumPeriodAggregationOutputDTO(
            dataset=[result["total"] for result in results],
            labels=[group_selector.convert_to_iso(result[self.document.id]) for result in results]
        )
