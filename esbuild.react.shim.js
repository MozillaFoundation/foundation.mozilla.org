/**
 * In order for ESBuild to correctly resolve the React.createElement()
 * function that babel "auto injects" when it transfroms JSX, we need
 * the following shim that ensures that any file that relies on React
 * has the variable "React" available for use.
 *
 * See https://esbuild.github.io/content-types/#auto-import-for-jsx
 */
export * as React from 'react'
