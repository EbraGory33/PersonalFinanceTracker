import AnimatedCounter from "./AnimatedCounter";
import DoughnutChart from "./DoughnutChart";

const TotalBalanceBox = ({
  accounts,
  total_banks,
  total_current_balance,
}: total_balance_box_props) => {
  return (
    <section className="total-balance">
      <div className="total-balance-chart">
        {/* DoughnutChart */}
        <DoughnutChart accounts={accounts} />
      </div>
      <div className="flex flex-col gap-6">
        <h2 className="header-2">Bank Accounts: {total_banks}</h2>
        <div className="flex flex-col gap-2">
          <p className="total-balance-label">Total Current Balance</p>

          <div className="total-balance-amount flex-center gap-2">
            <AnimatedCounter amount={total_current_balance} />
          </div>
        </div>
      </div>
    </section>
  );
};

export default TotalBalanceBox;
