import { App, TFile } from "obsidian";
import { Document } from "../models/Document";
import { Issue } from "../models/Issue";

/**
 * Base interface for all validators
 */
export interface Validator {
  /** Unique identifier for this validator */
  id: string;

  /** Human-readable name */
  name: string;

  /** Description of what this validator checks */
  description: string;

  /** Whether this validator needs global context (all files) */
  isGlobal: boolean;

  /** Validate a single document (for local validators) */
  validateFile?(document: Document, app: App): Promise<Issue[]>;

  /** Validate all documents (for global validators) */
  validateAll?(documents: Document[], app: App): Promise<Issue[]>;
}

/**
 * Base class for local validators (single file)
 */
export abstract class LocalValidator implements Validator {
  abstract id: string;
  abstract name: string;
  abstract description: string;
  isGlobal = false;

  abstract validateFile(document: Document, app: App): Promise<Issue[]>;
}

/**
 * Base class for global validators (need all files)
 */
export abstract class GlobalValidator implements Validator {
  abstract id: string;
  abstract name: string;
  abstract description: string;
  isGlobal = true;

  abstract validateAll(documents: Document[], app: App): Promise<Issue[]>;
}
