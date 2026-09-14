"use client";

import { useEffect, type RefObject } from "react";

/** Native dialogs supply focus containment and background inertness. */
export function useNativeDialog(
  open: boolean,
  dialogRef: RefObject<HTMLDialogElement | null>,
  initialFocus?: RefObject<HTMLElement | null>,
) {
  useEffect(() => {
    const dialog = dialogRef.current;
    if (!open || !dialog) return;
    const trigger = document.activeElement instanceof HTMLElement
      ? document.activeElement : null;
    const previousOverflow = document.documentElement.style.overflow;
    dialog.showModal();
    document.documentElement.style.overflow = "hidden";
    initialFocus?.current?.focus();
    return () => {
      dialog.close();
      document.documentElement.style.overflow = previousOverflow;
      if (trigger?.isConnected && trigger.getClientRects().length) trigger.focus();
    };
  }, [open, dialogRef, initialFocus]);
}
