import { apiFetch } from "@/utils/apiclients";

export const verify = async () => {
  try {
    const user = await apiFetch("auth/authenticate");
    return user;
  } catch (error) {
    console.error("Error", error);
  }
};

export const signIn = async ({ email, password }: signInProps) => {
  try {
    const user = await apiFetch("auth/signin", { email, password }, "POST");
    return user;
  } catch (error) {
    console.error("Error", error);
  }
};

export const signUp = async (params: SignUpParams) => {
  try {
    const user = await apiFetch("auth/signup", params, "POST");
    return user;
  } catch (error) {
    console.error("Error", error);
  }
};
