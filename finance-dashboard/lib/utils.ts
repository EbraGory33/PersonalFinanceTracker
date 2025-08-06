 
import { type ClassValue, clsx } from "clsx";
import qs from "query-string";
import { twMerge } from "tailwind-merge";
import { z } from "zod";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

// FORMAT DATE TIME
export const format_date_time = (date_string: Date) => {
  const date_time_options: Intl.DateTimeFormatOptions = {
    weekday: "short", // abbreviated weekday name (e.g., 'Mon')
    month: "short", // abbreviated month name (e.g., 'Oct')
    day: "numeric", // numeric day of the month (e.g., '25')
    hour: "numeric", // numeric hour (e.g., '8')
    minute: "numeric", // numeric minute (e.g., '30')
    hour12: true, // use 12-hour clock (true) or 24-hour clock (false)
  };

  const date_day_options: Intl.DateTimeFormatOptions = {
    weekday: "short", // abbreviated weekday name (e.g., 'Mon')
    year: "numeric", // numeric year (e.g., '2023')
    month: "2-digit", // abbreviated month name (e.g., 'Oct')
    day: "2-digit", // numeric day of the month (e.g., '25')
  };

  const date_options: Intl.DateTimeFormatOptions = {
    month: "short", // abbreviated month name (e.g., 'Oct')
    year: "numeric", // numeric year (e.g., '2023')
    day: "numeric", // numeric day of the month (e.g., '25')
  };

  const time_options: Intl.DateTimeFormatOptions = {
    hour: "numeric", // numeric hour (e.g., '8')
    minute: "numeric", // numeric minute (e.g., '30')
    hour12: true, // use 12-hour clock (true) or 24-hour clock (false)
  };

  const formatted_date_time: string = new Date(date_string).toLocaleString(
    "en-US",
    date_time_options
  );

  const formatted_date_day: string = new Date(date_string).toLocaleString(
    "en-US",
    date_day_options
  );

  const formatted_date: string = new Date(date_string).toLocaleString(
    "en-US",
    date_options
  );

  const formatted_time: string = new Date(date_string).toLocaleString(
    "en-US",
    time_options
  );

  return {
    date_time: formatted_date_time,
    date_day: formatted_date_day,
    date_only: formatted_date,
    time_only: formatted_time,
  };
};

export function format_amount(amount: number): string {
  const formatter = new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
    minimumFractionDigits: 2,
  });

  return formatter.format(amount);
}

export const parse_stringify = (value: unknown) =>
  JSON.parse(JSON.stringify(value));

export const remove_special_characters = (value: string) => {
  return value.replace(/[^\w\s]/gi, "");
};

interface Url_query_params {
  params: string;
  key: string;
  value: string;
}

export function form_url_query({ params, key, value }: Url_query_params) {
  const current_url = qs.parse(params);

  current_url[key] = value;

  return qs.stringifyUrl(
    {
      url: window.location.pathname,
      query: current_url,
    },
    { skipNull: true }
  );
}

export function get_account_type_colors(type: account_types) {
  switch (type) {
    case "depository":
      return {
        bg: "bg-blue-25",
        light_bg: "bg-blue-100",
        title: "text-blue-900",
        sub_text: "text-blue-700",
      };

    case "credit":
      return {
        bg: "bg-success-25",
        light_bg: "bg-success-100",
        title: "text-success-900",
        sub_text: "text-success-700",
      };

    default:
      return {
        bg: "bg-green-25",
        light_bg: "bg-green-100",
        title: "text-green-900",
        sub_text: "text-green-700",
      };
  }
}

export function count_transaction_categories(
  transactions: Transaction[]
): category_count[] {
  const category_counts: { [category: string]: number } = {};
  let total_count = 0;

  // Iterate over each transaction
  if (transactions) {
    transactions.forEach((transaction) => {
      const category = transaction.category;

      if (category_counts.hasOwnProperty(category)) {
        category_counts[category]++;
      } else {
        category_counts[category] = 1;
      }

      total_count++;
    });
  }

  // Convert the category_counts object to an array of objects
  const aggregated_categories: category_count[] = Object.keys(
    category_counts
  ).map((category) => ({
    name: category,
    count: category_counts[category],
    total_count,
  }));

  // Sort the aggregated_categories array by count in descending order
  aggregated_categories.sort((a, b) => b.count - a.count);

  return aggregated_categories;
}

export function extract_customer_id_from_url(url: string) {
  // Split the URL string by '/'
  const parts = url.split("/");

  // Extract the last part, which represents the customer ID
  const customer_id = parts[parts.length - 1];

  return customer_id;
}

export function encrypt_id(id: string) {
  return btoa(id);
}

export function decrypt_id(id: string) {
  return atob(id);
}

export const get_transaction_status = (date: Date) => {
  const today = new Date();
  const two_days_ago = new Date(today);
  two_days_ago.setDate(today.getDate() - 2);

  return date > two_days_ago ? "Processing" : "Success";
};

export const auth_form_schema = (type: string) =>
  z.object({
    // sign up fields
    first_name:
      type === "sign-in"
        ? z.string().optional()
        : z
            .string()
            .min(3, { message: "First name must be at least 3 characters." }),
    last_name:
      type === "sign-in"
        ? z.string().optional()
        : z
            .string()
            .min(3, { message: "Last name must be at least 3 characters." }),
    address1:
      type === "sign-in"
        ? z.string().optional()
        : z
            .string()
            .max(50, { message: "Address must be at most 50 characters." }),
    city:
      type === "sign-in"
        ? z.string().optional()
        : z
            .string()
            .max(50, { message: "City must be at most 50 characters." }),
    state:
      type === "sign-in"
        ? z.string().optional()
        : z
            .string()
            .min(2, { message: "State must be exactly 2 characters." })
            .max(2, { message: "State must be exactly 2 characters." }),
    postal_code:
      type === "sign-in"
        ? z.string().optional()
        : z
            .string()
            .min(3, { message: "Postal code must be at least 3 characters." })
            .max(6, { message: "Postal code must be at most 6 characters." }),
    date_of_birth:
      type === "sign-in"
        ? z.string().optional()
        : z.string().min(3, {
            message: "Date of birth must be at least 3 characters.",
          }),
    ssn:
      type === "sign-in"
        ? z.string().optional()
        : z.string().min(3, { message: "SSN must be at least 3 characters." }),

    // both
    email: z.email({ message: "Please enter a valid email address." }),
    password: z
      .string()
      .min(8, { message: "Password must be at least 8 characters." }),
  });
