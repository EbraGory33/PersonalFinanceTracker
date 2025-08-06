declare type search_param_props = {
  params: { [key: string]: string };
  search_params: { [key: string]: string | string[] | undefined };
};

declare type sign_up_params = {
  first_name: string;
  last_name: string;
  address1: string;
  city: string;
  state: string;
  postal_code: string;
  date_of_birth: string;
  ssn: string;
  email: string;
  password: string;
};

declare type login_user = {
  email: string;
  password: string;
};

declare type user = {
  id: number;
  email: string;
  user_id: string;
  dwolla_customer_url: string;
  dwolla_customer_id: string;
  first_name: string;
  last_name: string;
  address1: string;
  city: string;
  state: string;
  postal_code: string;
  date_of_birth: string;
  ssn: string;
  is_active: boolean;
};

declare type new_user_params = {
  user_id: string;
  email: string;
  name: string;
  password: string;
};

declare type account = {
  data: AccountData;
  transactions: transaction[];
};

declare type accounts_response = {
  accounts: AccountData[];
  total_banks: number;
  total_current_balance: number;
};

declare type AccountData = {
  id: string;
  available_balance: number;
  current_balance: number;
  institutionId: string;
  name: string;
  officialName: string;
  mask: string;
  type: string;
  subtype: string;
  bank_id: number;
  shareable_id: string;
};

declare type Transaction = {
  id: string;
  name: string;
  payment_channel: string;
  type: string;
  accountId: string;
  amount: number;
  pending: boolean;
  category: string;
  date: string;
  sender_id: number | null;
  receiver_id: number | null;
  sender_bank_id: number | null;
  receiver_bank_id: number | null;
  image: string | null;
};

declare type AccountWithTransactions = {
  data: AccountData;
  transactions: Transaction[];
};

declare type banks = {
  banks: bank[];
};

declare type bank = {
  id: number;
  user_id: number;
  bank_id: string;
  account_id: string;
  access_token: string;
  funding_source_url: string;
  shareable_id: string;
};

declare type account_types =
  | "depository"
  | "credit"
  | "loan "
  | "investment"
  | "other";

declare type category = "Food and Drink" | "Travel" | "Transfer";

declare type category_count = {
  name: string;
  count: number;
  total_count: number;
};

declare type receiver = {
  first_name: string;
  last_name: string;
};

declare type transfer_params = {
  source_funding_source_url: string;
  destination_funding_source_url: string;
  amount: string;
};

declare type add_funding_source_params = {
  dwolla_customer_id: string;
  processor_token: string;
  bank_name: string;
};

declare type new_dwolla_customer_params = {
  first_name: string;
  last_name: string;
  email: string;
  type: string;
  address1: string;
  city: string;
  state: string;
  postal_code: string;
  date_of_birth: string;
  ssn: string;
};

declare interface credit_card_props {
  account: AccountData;
  user_name: string;
  show_balance?: boolean;
}

declare interface bank_info_props {
  account: AccountData;
  shareable_id?: string;
  type: "full" | "card";
}

declare interface header_box_props {
  type?: "title" | "greeting";
  title: string;
  subtext: string;
  user?: string;
}

declare interface mobile_nav_props {
  user: user | [];
}

declare interface page_header_props {
  top_title: string;
  bottom_title: string;
  top_description: string;
  bottom_description: string;
  connect_bank?: boolean;
}

declare interface pagination_props {
  page: number;
  total_pages: number;
}

declare interface plaid_link_props {
  user: user;
  variant?: "primary" | "ghost";
  dwolla_customer_id?: string;
}

declare interface auth_form_props {
  type: "sign-in" | "sign-up";
}

declare interface bank_dropdown_props {
  accounts: AccountData[];
  set_value?: UseFormSetValue<any>;
  other_styles?: string;
}

declare interface bank_tab_item_props {
  account: AccountData;
  shareable_id?: string;
}

declare interface total_balance_box_props {
  accounts: AccountData[];
  total_banks: number;
  total_current_balance: number;
}

declare interface footer_props {
  user: user | [];
  type?: "mobile" | "desktop";
}

declare interface right_sidebar_props {
  user: user | [];
  transactions: transaction[];
  banks: AccountData[];
}

declare interface siderbar_props {
  user: user;
}

declare interface recent_transactions_props {
  accounts: AccountData[];
  transactions: transaction[];
  shareable_id: string;
  page: number;
}

declare interface transaction_history_table_props {
  transactions: Transaction[];
  page: number;
}

declare interface category_badge_props {
  category: string;
}

declare interface transaction_table_props {
  transactions: Transaction[];
}

declare interface category_props {
  category: category_count;
}

declare interface doughnut_chart_props {
  accounts: AccountData[];
}

declare interface payment_transfer_form_props {
  accounts: AccountData[];
}

declare interface get_accounts_props {
  user_id: string;
}

declare interface get_account_props {
  appwrite_item_id: string;
}

declare interface get_institution_props {
  institution_id: string;
}

declare interface get_transactions_props {
  access_token: string;
}

declare interface create_funding_source_options {
  customer_id: string;
  funding_source_name: string;
  plaid_token: string;
  _links: object;
}

declare interface create_transaction_props {
  name: string;
  amount: number;
  sender_id: number;
  sender_bank_id: number;
  receiver_id: number;
  receiver_bank_id: number;
  email: string;
}

declare interface get_transactions_by_bank_id_props {
  bank_id: string;
}

declare interface sign_in_props {
  email: string;
  password: string;
}

declare interface get_user_info_props {
  user_id: string;
}

declare interface exchange_public_token_props {
  public_token: string;
}

declare interface create_bank_account_props {
  access_token: string;
  user_id: string;
  account_id: string;
  bank_id: string;
  funding_source_url: string;
  sharable_id: string;
}

declare interface get_banks_props {
  user_id: string;
}

declare interface get_bank_props {
  document_id: string;
}

declare interface get_bank_by_account_id_props {
  account_id: string;
}
