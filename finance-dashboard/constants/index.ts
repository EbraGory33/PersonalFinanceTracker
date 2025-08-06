export const sidebar_links = [
  {
    img_url: "/icons/home.svg",
    route: "/",
    label: "Home",
  },
  {
    img_url: "/icons/dollar-circle.svg",
    route: "/my-banks",
    label: "My Banks",
  },
  {
    img_url: "/icons/transaction.svg",
    route: "/transaction-history",
    label: "Transaction History",
  },
  {
    img_url: "/icons/money-send.svg",
    route: "/payment-transfer",
    label: "Transfer Funds",
  },
];

// good_user / good_password - Bank of America
// export const test_user_id = "6627ed3d00267aa6fa3e";

// custom_user -> Chase Bank
// export const test_access_token =
//   "access-sandbox-da44dac8-7d31-4f66-ab36-2238d63a3017";

// custom_user -> Chase Bank
// export const test_access_token =
//   "access-sandbox-229476cf-25bc-46d2-9ed5-fba9df7a5d63";

// export const items = [
//   {
//     id: "6624c02e00367128945e", // appwrite item Id
//     access_token: "access-sandbox-83fd9200-0165-4ef8-afde-65744b9d1548",
//     item_id: "VPMQJKG5vASvpX8B6JK3HmXkZlAyplhW3r9xm",
//     user_id: "6627ed3d00267aa6fa3e",
//     account_id: "X7LMJkE5vnskJBxwPeXaUWDBxAyZXwi9DNEWJ",
//   },
//   {
//     id: "6627f07b00348f242ea9", // appwrite item Id
//     access_token: "access-sandbox-74d49e15-fc3b-4d10-a5e7-be4ddae05b30",
//     item_id: "Wv7P6vNXRXiMkoKWPzeZS9Zm5JGWdXulLRNBq",
//     user_id: "6627ed3d00267aa6fa3e",
//     account_id: "x1GQb1lDrDHWX4BwkqQbI4qpQP1lL6tJ3VVo9",
//   },
// ];

export const top_category_styles = {
  "Food and Drink": {
    bg: "bg-blue-25",
    circle_bg: "bg-blue-100",
    text: {
      main: "text-blue-900",
      count: "text-blue-700",
    },
    progress: {
      bg: "bg-blue-100",
      indicator: "bg-blue-700",
    },
    icon: "/icons/monitor.svg",
  },
  Travel: {
    bg: "bg-success-25",
    circle_bg: "bg-success-100",
    text: {
      main: "text-success-900",
      count: "text-success-700",
    },
    progress: {
      bg: "bg-success-100",
      indicator: "bg-success-700",
    },
    icon: "/icons/coins.svg",
  },
  default: {
    bg: "bg-pink-25",
    circle_bg: "bg-pink-100",
    text: {
      main: "text-pink-900",
      count: "text-pink-700",
    },
    progress: {
      bg: "bg-pink-100",
      indicator: "bg-pink-700",
    },
    icon: "/icons/shopping-bag.svg",
  },
};

export const transaction_category_styles = {
  "Food and Drink": {
    border_color: "border-pink-600",
    background_color: "bg-pink-500",
    text_color: "text-pink-700",
    chip_background_color: "bg-inherit",
  },
  Payment: {
    border_color: "border-success-600",
    background_color: "bg-green-600",
    text_color: "text-success-700",
    chip_background_color: "bg-inherit",
  },
  "Bank Fees": {
    border_color: "border-success-600",
    background_color: "bg-green-600",
    text_color: "text-success-700",
    chip_background_color: "bg-inherit",
  },
  Transfer: {
    border_color: "border-red-700",
    background_color: "bg-red-700",
    text_color: "text-red-700",
    chip_background_color: "bg-inherit",
  },
  Processing: {
    border_color: "border-[#F2F4F7]",
    background_color: "bg-gray-500",
    text_color: "text-[#344054]",
    chip_background_color: "bg-[#F2F4F7]",
  },
  Success: {
    border_color: "border-[#12B76A]",
    background_color: "bg-[#12B76A]",
    text_color: "text-[#027A48]",
    chip_background_color: "bg-[#ECFDF3]",
  },
  default: {
    border_color: "",
    background_color: "bg-blue-500",
    text_color: "text-blue-700",
    chip_background_color: "bg-inherit",
  },
};
