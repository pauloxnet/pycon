/** @jsxRuntime classic */

/** @jsx jsx */
import { useCallback } from "react";
import { FormattedMessage } from "react-intl";
import { useFormState } from "react-use-form-state";
import { Box, Button, Heading, Input, jsx } from "theme-ui";

import { GetStaticPaths, GetStaticProps } from "next";
import { useRouter } from "next/router";

import { addApolloState, getApolloClient } from "~/apollo/client";
import { Alert } from "~/components/alert";
import { InputWrapper } from "~/components/input-wrapper";
import { prefetchSharedQueries } from "~/helpers/prefetch";
import { useMessages } from "~/helpers/use-messages";
import { useTranslatedMessage } from "~/helpers/use-translated-message";
import { useResetPasswordMutation } from "~/types";

type FormFields = {
  password: string;
};

export const ResetPasswordPage = () => {
  const router = useRouter();
  const { addMessage } = useMessages();
  const successMessage = useTranslatedMessage("resetPassword.youCanNowLogin");

  const [changePassword, { loading, error, data }] = useResetPasswordMutation({
    onCompleted(data) {
      if (
        data?.resetPassword.__typename === "OperationSuccess" &&
        data.resetPassword.ok
      ) {
        addMessage({
          message: successMessage,
          type: "success",
        });

        router.push("/login");
      }
    },
  });
  const [formState, { password }] = useFormState<FormFields>(
    {},
    {
      withIds: true,
    },
  );

  const token = router.query.token as string;
  const userId = router.query.userId as string;

  const onSubmit = useCallback(
    (e) => {
      e.preventDefault();

      if (loading) {
        return;
      }

      changePassword({
        variables: {
          token,
          password: formState.values.password,
        },
      });
    },
    [formState, loading, token, userId],
  );

  const getErrors = (key: "token" | "password") =>
    (data?.resetPassword.__typename === "ResetPasswordValidationError" &&
      (data?.resetPassword[key] ?? []).map((e) => e.message)) ||
    [];

  const tokenErrors = getErrors("token");

  return (
    <Box
      as="form"
      sx={{
        maxWidth: "container",
        mx: "auto",
        px: 3,
      }}
      onSubmit={onSubmit}
    >
      {error && <Alert variant="alert">{error.message}</Alert>}
      {tokenErrors.length > 0 && (
        <Alert variant="alert">{tokenErrors.join(", ")}</Alert>
      )}

      <Heading mb={4} as="h1">
        <FormattedMessage id="resetPassword.changeYourPassword" />
      </Heading>

      <InputWrapper
        errors={getErrors("password")}
        sx={{
          mb: 3,
        }}
        label={<FormattedMessage id="resetPassword.newPassword" />}
      >
        <Input {...password("password")} />
      </InputWrapper>
      <Button>
        <FormattedMessage id="resetPassword.changePassword" />
      </Button>
    </Box>
  );
};

export const getStaticProps: GetStaticProps = async ({ locale }) => {
  const client = getApolloClient();

  await prefetchSharedQueries(client, locale);

  return addApolloState(client, {
    props: {},
  });
};

export const getStaticPaths: GetStaticPaths = async () =>
  Promise.resolve({
    paths: [],
    fallback: "blocking",
  });

export default ResetPasswordPage;
