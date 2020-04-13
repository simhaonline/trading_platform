from core.portfolio import Portfolio

from core.trading import Trading
from core.configuration import Configuration
from datahandlers.data_handler_factory import DataHandlerFactory
from datahandlers.zmq_data_handler import ZmqDataHandler
from executionhandlers.oanda_execution import OandaExecutionHandler
from executionhandlers.execution_handler_factory import ExecutionHandlerFactory
from strategies.no_trading_strategy import NoTradingStrategy
from positionsizehandlers.fixed_position_size import FixedPositionSize
from loggers.text_logger import TextLogger


def get_strategy():
    return NoTradingStrategy


def main():

    strategy = get_strategy()
    args_namespace = strategy.create_argument_parser(False).parse_args()

    events_log_file = '{}/events.log'.format(args_namespace.output_directory)

    strategy_params = strategy.get_strategy_params(args_namespace)

    configuration = Configuration(data_handler_name=ZmqDataHandler, execution_handler_name=OandaExecutionHandler)
    configuration.set_option(Configuration.OPTION_TIMEFRAME, args_namespace.time_frame)

    trading = Trading(args_namespace.output_directory, list(args_namespace.symbols), 0,
                      configuration, DataHandlerFactory(), ExecutionHandlerFactory(), Portfolio, strategy,
                      FixedPositionSize(0.01), TextLogger(events_log_file), [Trading.LOG_TYPE_EVENTS], strategy_params,
                      'equity.csv', 'trades.csv')

    trading.run()
    trading.print_performance()


if __name__ == "__main__":
    main()