from collections import defaultdict

from src.domain.abc.dal import DocumentDAO
from src.domain.payment.dto import PaymentCreateDTO, PaymentUpdateDTO, SumPeriodGroupEnum, SumByPeriodOutputDTO
from src.domain.payment.model import Payment
from src.domain.payment.dal.constructor.sum_by_period import SumByPeriodGroupingSelector
from src.domain.period.dto import PeriodDTO


class PaymentDAO(DocumentDAO[Payment, PaymentCreateDTO, PaymentUpdateDTO]):
    document = Payment
    create_dto = PaymentCreateDTO
    update_dto = PaymentUpdateDTO

    async def get_sum_by_period(self, period: PeriodDTO, group_type: SumPeriodGroupEnum) -> SumByPeriodOutputDTO:
        grouping_strategy = SumByPeriodGroupingSelector(period, group_type)
        period = grouping_strategy.period

        pipeline = [
            {
                "$match": grouping_strategy.match
            },
            {
                "$group": grouping_strategy.group
            },
            {
                "$sort": grouping_strategy.sort
            }
        ]

        results = await self.document.aggregate(pipeline).to_list(length=None)

        sums = defaultdict(int)
        for result in results:
            label = grouping_strategy.convert_to_iso(result[self.document.id])
            sums[label] = result["total"]

        current = period.from_dt
        labels = []
        dataset = []

        while current <= period.to_dt:
            label = current.isoformat()
            labels.append(label)
            dataset.append(sums[label])
            current = grouping_strategy.increment(current)

        return SumByPeriodOutputDTO(dataset=dataset, labels=labels)
