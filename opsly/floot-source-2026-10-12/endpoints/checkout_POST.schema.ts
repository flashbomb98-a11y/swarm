import { z } from "zod";
import superjson from "superjson";
import { productCatalog } from "../helpers/productCatalog";

export const schema = z.object({
  productId: z.enum(Object.keys(productCatalog) as [keyof typeof productCatalog, ...(keyof typeof productCatalog)[]]),
});
export type InputType = z.infer<typeof schema>;
export type OutputType = { checkoutUrl: string };

export const postCheckout = async (body: InputType): Promise<OutputType> => {
  const validated = schema.parse(body);
  const result = await fetch("/_api/checkout", {
    method: "POST",
    body: superjson.stringify(validated),
    headers: { "Content-Type": "application/json" },
  });
  if (!result.ok) {
    const err = superjson.parse<{error:string}>(await result.text());
    throw new Error(err.error);
  }
  return superjson.parse<OutputType>(await result.text());
};
