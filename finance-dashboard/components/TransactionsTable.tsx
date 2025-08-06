import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { transaction_category_styles } from "@/constants";
import {
  cn,
  format_amount,
  format_date_time,
  get_transaction_status,
  remove_special_characters,
} from "@/lib/utils";

const CategoryBadge = ({ category }: category_badge_props) => {
  const { border_color, background_color, text_color, chip_background_color } =
    transaction_category_styles[
      category as keyof typeof transaction_category_styles
    ] || transaction_category_styles.default;

  return (
    <div className={cn("category-badge", border_color, chip_background_color)}>
      <div className={cn("size-2 rounded-full", background_color)} />
      <p className={cn("text-[12px] font-medium", text_color)}>{category}</p>
    </div>
  );
};

const TransactionsTable = ({ transactions }: transaction_table_props) => {
  return (
    <Table>
      <TableHeader className="bg-[#f9fafb]">
        <TableRow>
          <TableHead className="px-2">Transaction</TableHead>
          <TableHead className="px-2">Amount</TableHead>
          <TableHead className="px-2">Status</TableHead>
          <TableHead className="px-2">Date</TableHead>
          <TableHead className="px-2 max-md:hidden">Channel</TableHead>
          <TableHead className="px-2 max-md:hidden">Category</TableHead>
        </TableRow>
      </TableHeader>
      <TableBody>
        {transactions.map((t: Transaction) => {
          const status = get_transaction_status(new Date(t.date));
          const amount = format_amount(t.amount);

          const isDebit = t.type === "debit";
          const isCredit = t.type === "credit";

          return (
            <TableRow
              key={t.id}
              className={`${
                isDebit || amount[0] === "-" ? "bg-[#FFFBFA]" : "bg-[#F6FEF9]"
              } !over:bg-none !border-b-DEFAULT`}
            >
              <TableCell className="max-w-[250px] pl-2 pr-10">
                <div className="flex items-center gap-3">
                  <h1 className="text-14 truncate font-semibold text-[#344054]">
                    {remove_special_characters(t.name)}
                  </h1>
                </div>
              </TableCell>

              <TableCell
                className={`pl-2 pr-10 font-semibold ${
                  isDebit || amount[0] === "-"
                    ? "text-[#f04438]"
                    : "text-[#039855]"
                }`}
              >
                {isDebit ? `-${amount}` : isCredit ? amount : amount}
              </TableCell>

              <TableCell className="pl-2 pr-10">
                <CategoryBadge category={status} />
              </TableCell>

              <TableCell className="min-w-32 pl-2 pr-10">
                {format_date_time(new Date(t.date)).date_time}
              </TableCell>

              <TableCell className="pl-2 pr-10 capitalize min-w-24">
                {t.payment_channel}
              </TableCell>

              <TableCell className="pl-2 pr-10 max-md:hidden">
                <CategoryBadge category={t.category} />
              </TableCell>
            </TableRow>
          );
        })}
      </TableBody>
    </Table>
  );
};

export default TransactionsTable;
