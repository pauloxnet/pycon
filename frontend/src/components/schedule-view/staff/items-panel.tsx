/** @jsxRuntime classic */

/** @jsx jsx */
import React, { useState } from "react";
import { Box, Heading, Input, jsx } from "theme-ui";

import {
  AllTracksEvent,
  CustomEvent,
  Keynote,
  RoomChangeEvent,
  Submission,
} from "../events";
import { Submission as SubmissionType, Keynote as KeynoteType } from "../types";

type ItemsPanelProp = {
  submissions: SubmissionType[];
  keynotes: KeynoteType[];
};

export const ItemsPanel = ({ submissions, keynotes }: ItemsPanelProp) => {
  const [query, setQuery] = useState("");

  // TODO: https://fusejs.io/
  const filteredSubmissions = submissions.filter((submission) =>
    submission.title.toLowerCase().includes(query),
  );

  return (
    <Box
      sx={
        {
          position: "fixed",
          bottom: 0,
          top: 0,
          right: 0,
          zIndex: "scheduleItemPanel",
          width: 300,
          p: 4,
          borderLeft: "primary",
          background: "white",
          overflowX: "scroll",
        } as any
      }
    >
      <Heading sx={{ mb: 4 }}>Special items</Heading>

      <AllTracksEvent sx={{ mb: 4, width: "100%" }} />
      <RoomChangeEvent sx={{ mb: 4, width: "100%" }} />
      <CustomEvent sx={{ mb: 4, width: "100%" }} />

      <Heading sx={{ mb: 4 }}>Keynotes</Heading>

      {keynotes.map((keynote) => (
        <Keynote sx={{ mb: 3, width: "100%" }} keynote={keynote} />
      ))}

      <Heading sx={{ my: 4 }}>Submissions</Heading>

      <Box>
        <Input
          type="search"
          placeholder="Filter submissions"
          value={query}
          onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
            setQuery(e.target.value)
          }
          sx={{ mb: 4 }}
        />
        {filteredSubmissions.map((submission) => (
          <Submission
            submission={submission}
            key={submission.id}
            sx={{ mb: 3, width: "100%" }}
          />
        ))}
      </Box>
    </Box>
  );
};
