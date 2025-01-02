import { pick } from "lodash"

const propTypes = {
  resource_name: {
    type: String,
    required: true,
  },
  resource_id: {
    type: String,
    required: false,
  },
  should_override_meta: {
    type: Boolean,
    required: false,
  }
}

export const mapProps = (props: Array<string>) => pick(propTypes, props)