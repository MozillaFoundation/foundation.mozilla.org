import { Localized } from "@fluent/react";

function Customized(props) {
  if (props.stringId) {
    const { stringId, ...newprops } = props;
    newprops.id = stringId;
    return Localized(newprops);
  }

  return Localized(props);
}

export { Customized as Localized };
