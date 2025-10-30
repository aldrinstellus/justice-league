import { type ClassValue, clsx } from "clsx"
import { twMerge } from "tailwind-merge"

/**
 * Merge Tailwind CSS classes with proper conflict resolution
 *
 * This utility combines clsx for conditional class handling and tailwind-merge
 * for intelligent Tailwind class conflict resolution. It ensures that later
 * classes properly override earlier ones, solving the component style conflict
 * issue identified in the Settings conversion.
 *
 * @example
 * ```tsx
 * // Later classes override earlier ones
 * cn("bg-white", "bg-black") // Returns: "bg-black"
 *
 * // Conditional classes
 * cn("text-base", { "text-lg": isLarge, "text-sm": isSmall })
 *
 * // Component with default styles that can be overridden
 * function Card({ className, ...props }) {
 *   return <div className={cn("bg-white rounded-lg", className)} {...props} />
 * }
 * // Usage: <Card className="bg-black" /> // Will be black, not white
 * ```
 *
 * Learned from: Settings conversion - iteration 2, 4
 * Issue: Card and Button components had hardcoded bg-white and bg-zinc-900
 * Solution: Use cn() to allow className prop to override component defaults
 */
export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}
