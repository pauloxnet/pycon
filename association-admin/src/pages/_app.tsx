import { dedupExchange, cacheExchange, fetchExchange } from "@urql/core";
import { authExchange } from "@urql/exchange-auth";
import { RecoilRoot } from "recoil";
import { makeOperation } from "urql";

import { withUrqlClient } from "next-urql";
import Router from "next/router";

import { Drawer } from "~/components/drawer";
import { UserProvider } from "~/components/user-provider";
import { getToken } from "~/hooks/use-user";

import "tailwindcss/tailwind.css";

const App = ({ Component, pageProps }) => (
  <RecoilRoot>
    <UserProvider>
      <div className="h-screen w-screen flex overflow-hidden bg-white">
        <Drawer />
        <Component {...pageProps} />
      </div>
    </UserProvider>
  </RecoilRoot>
);

export default withUrqlClient(
  (ssrExchange, ctx) => ({
    url: "/graphql",
    exchanges: [
      dedupExchange,
      cacheExchange,
      ssrExchange,
      authExchange({
        didAuthError({ error }) {
          return error.graphQLErrors.some((e) => e.message === "Unauthorized");
        },
        async getAuth({ authState }) {
          if (!authState) {
            const token = typeof window !== "undefined" && getToken();

            if (token) {
              return { token };
            }
          }

          Router.replace("/logout");

          return null;
        },
        addAuthToOperation({ authState, operation }) {
          if (!authState || !authState.token) {
            return operation;
          }

          const fetchOptions =
            typeof operation.context.fetchOptions === "function"
              ? operation.context.fetchOptions()
              : operation.context.fetchOptions || {};

          console.log("aaa", operation);
          return makeOperation(operation.kind, operation, {
            ...operation.context,
            fetchOptions: {
              ...fetchOptions,
              credentials: "include",
              headers: {
                ...fetchOptions.headers,
                Authorization: `Bearer ${authState.token}`,
              },
            },
          });
        },
      }),
      fetchExchange,
    ],
  }),
  { ssr: false },
)(App);
